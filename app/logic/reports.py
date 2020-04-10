from ..config import cfg
from ..db import *
from .file_storage import reports_manager

from flask import abort
import logging


# Legacy
# def get_report(e_id, r_id):
#     with get_session() as s:
#         event = s.query(Event).get(e_id)
#         if not event or event.status == 'deleted':
#             abort(404, 'No event with this id')

#         report = s.query(Participation, User).filter(
#                 User.id == Participation.u_id,
#                 Participation.id == r_id,
#                 Participation.participation_role == 'presenter'
#         ).one_or_none()

#         if not report:
#             abort(404, 'Report not found by this id')

#         return {
#             'email': report.User.email,
#             'name': report.User.name,
#             'surname': report.User.surname,
#             "report": report.Participation.report,
#             "presenter_description": report.Participation.presenter_description,
#             "report_description": report.Participation.report_description,
#             "report_status": report.Participation.report_status
#         }

def upload_report(u_id, e_id, file):
    with get_session() as s:
        event = s.query(Event).get(e_id)
        if not event or event.status == 'deleted':
            abort(404, 'No event with this id')
        participation = s.query(Participation).filter(
            Participation.u_id == u_id,
            Participation.e_id == e_id
        ).one_or_none()

        if not participation:
            abort(424, 'User must join event before uploading')

        report_id = participation.report_id
        filename = file.filename
        if report_id is not None:
            reports_manager.remove(report_id)
        report_id = reports_manager.save(file)
        participation.report_id = report_id
        participation.report_name = filename
        logging.info(
            'User [id {u_id}] uploaded report file '
            '[{fname}] for event [id {e_id}].'
            'Saved [id {r_id}]'.format(
                u_id = u_id,
                e_id = e_id,
                fname = filename,
                r_id = report_id
            )
        )
        return report_id

def get_all_reports():
    with get_session() as s:
        return list(
                map(
                lambda r: {
                    "event_id": r.e_id,
                    "user_id": r.u_id,
                    "report_id": r.report_id,
                    "name": r.report_name,
                    "last_update": r.last_updated,
                    "status": r.report_status
                },
                s.query(Participation).add_columns(
                    Participation.e_id,
                    Participation.u_id,
                    Participation.report_name,
                    Participation.report_name,
                    Participation.last_updated,
                    Participation.report_status,
                    Participation.report_id,
                ).filter(
                    Participation.report_id != None
                ).all()
            )
        )

def get_report(u_id, e_id):
    with get_session() as s:
        event = s.query(Event).get(e_id)
        if not event or event.status == 'deleted':
            abort(404, 'No event with this id')
        participation = s.query(Participation).filter(
            Participation.u_id == u_id,
            Participation.e_id == e_id
        ).one_or_none()
        if not participation:
            abort(424, 'User not joined')
        if participation.report_id is None:
            abort(404, 'No report found')
        return (*reports_manager.get(participation.report_id), participation.report_name)

def get_report_by_id(r_id):
    with get_session() as s:
        participation = s.query(Participation).filter(
            Participation.report_id == r_id,
        ).one_or_none()
        if participation.report_id is None:
            abort(404, 'No report found')
        return (*reports_manager.get(participation.report_id), participation.report_name)

def get_report_info(u_id, e_id):
    with get_session() as s:
        event = s.query(Event).get(e_id)
        if not event or event.status == 'deleted':
            abort(404, 'No event with this id')
        participation = s.query(Participation).filter(
            Participation.u_id == u_id,
            Participation.e_id == e_id,
            Participation.participation_role == 'presenter'
        ).one_or_none()
        if not participation:
            abort(424, 'User not joined')
        if participation.report_id is None:
            abort(404, 'No report found')
        result = {}
        result['report_id'] = participation.report_id
        result['report_name'] = participation.report_name
        result['last_updated'] = participation.last_updated
        result['status'] = participation.report_status
        return result

def get_reports_for_event(e_id):
    with get_session() as s:
        event = s.query(Event).get(e_id)
        if not event or event.status == 'deleted':
            abort(404, 'No event with this id')
        participations = s.query(Participation).filter(
            Participation.e_id == e_id,
            Participation.participation_role == 'presenter',
            Participation.report_status == 'approved'
        ).all()
        if len(participations) == 0 :
            abort(404, 'No participants found')
        if all(
            participation.report_id == None for participation in participations
        ):
            abort(404, 'No reports found')
        
        return list(
            map(
                lambda p: {
                    'report_id': p.report_id,
                    'report_name': p.report_name,
                    'last_updated': p.last_updated,
                },
                participations
            )
        )

def get_report_for_event_admin(e_id):
    with get_session() as s:
        event = s.query(Event).get(e_id)
        if not event or event.status == 'deleted':
            abort(404, 'No event with this id')
        participations = s.query(Participation).filter(
            Participation.e_id == e_id,
            Participation.participation_role == 'presenter' 
        ).all()
        if len(participations) == 0:
            abort(404, 'No participants founde')
        if all(
            participation.report_id == None for participation in participations
        ):
            abort(404, 'No reports found')
        
        return list(
            map(
                lambda p: {
                    'report_id': p.report_id,
                    'report_name': p.report_name,
                    'last_updated': p.last_updated,
                    'status': p.report_status
                },
                participations
            )
        )

def remove_report(u_id, e_id):
    with get_session() as s:
        event = s.query(Event).get(e_id)
        if not event or event.status == 'deleted':
            abort(404, 'No event with this id')
        participation = s.query(Participation).filter(
            Participation.u_id == u_id,
            Participation.e_id == e_id
        ).one_or_none()
        if not participation:
            abort(424, "User hasn't joined the event")
        report_id = participation.report_id
        if report_id is None:
            abort(404, 'No report found')
        participation.report_id = None
        participation.report_name = None
        reports_manager.remove(report_id)
        logging.info(
            'User [id {u_id}] deleted report [id {r_id}]'.format(
                u_id = u_id,
                r_id = report_id
            )
        )
