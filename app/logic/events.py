from ..config import cfg
from ..db import *
from .. import util

import logging

from sqlalchemy.exc import IntegrityError
from sqlalchemy import desc, or_

from flask import abort
from datetime import date, time, timezone
import requests
import os
import nanoid


def get_event_info(e_id):
    with get_session() as s:
        event = s.query(Event, Participation, User).filter(
                Event.id == e_id,
                Participation.e_id == Event.id,
                Event.status == 'active',
                Participation.u_id == User.id,
                Participation.participation_role == 'creator'
        ).first()

        if not event:
            abort(404, 'No event with this id')

        return {
            "creator_email": event.User.email,
            "phone": event.User.phone,
            "name": event.Event.name,
            "sm_description": event.Event.sm_description,
            "description": event.Event.description,
            "start_date": event.Event.start_date.isoformat(),
            "end_date": event.Event.end_date.isoformat(),
            "start_time": event.Event.start_time.isoformat(),
            "location": event.Event.location,
            "site_link": event.Event.site_link,
            "additional_info": event.Event.additional_info
        }


def get_events(offset, size):
    result = []
    with get_session() as s:
        events = s.query(Event).filter(Event.status == 'active').order_by(desc(Event.start_date))
        if offset and size:
            offset = int(offset)
            size = int(size)
            if offset < 0 or size < 1:
                abort(422, 'Offset or size has wrong values')
            events = events.slice(offset, offset+size)
        elif not offset and not size:
            events = events.all()
        else:
            abort(400, 'Wrong query string arg')

        for event in events:
            result.append({
                'id': event.id,
                'name': event.name,
                'sm_description': event.sm_description,
                'start_date': event.start_date.isoformat(),
                'end_date': event.end_date.isoformat(),
                'start_time': event.start_time.isoformat(),
                'location': event.location,
                'site_link': event.site_link
            })
    return result


def create_event(u_id, data):
    start_date = data['start_date'].split('-')
    date_start = date(int(start_date[0]), int(start_date[1]), int(start_date[2]))
    end_date = data['end_date'].split('-')
    date_end = date(int(end_date[0]), int(end_date[1]), int(end_date[2]))
    start_time = data['start_time'].split(':')
    time_start = time(int(start_time[0]), int(start_time[1]), 0, 0, timezone.utc)
    
    with get_session() as s:
        event = Event(name=data['name'], sm_description=data['sm_description'],
                      description=data['description'], start_date=date_start,
                      end_date=date_end, start_time=time_start,
                      location=data['location'], site_link=data['site_link'],
                      additional_info=data['additional_info'])
        s.add(event)
        s.flush()
        s.refresh(event)
        participation = Participation(e_id=event.id, u_id=u_id,
                                      participation_role='creator')
        s.add(participation)

        logging.info('Creating event [{}] [{}] [{}] [{}]'.format(data['name'],
                                                                 date_start,
                                                                 date_end,
                                                                 start_time))
        return event.id


def add_manager(e_id, data):
    with get_session() as s:
        event = s.query(Event).get(e_id)
        if not event or event.status == 'deleted':
            abort(404, 'No event with this id')

        user = s.query(User).filter(
                User.email == data['email'],
                User.status == 'active'
        ).one_or_none()
        if not user:
            abort(404, 'No user with this id')

        part = s.query(Participation).filter(
                Participation.u_id == user.id,
                Participation.e_id == e_id
        ).one_or_none()
        if part:
            abort(409, 'User has already joined this event as [{}]'.format(part.participation_role))

        manager = s.query(Participation).filter(
                Participation.e_id == e_id,
                Participation.participation_role == 'manager'
        ).one_or_none()
        if not manager:
            add = Participation(e_id=e_id, u_id=user.id,
                                      participation_role='manager')
            s.add(add)
            return 'added'
        else:
            if manager.u_id == user.id:
                abort(409, 'User has already added as manager')
            manager.u_id = user.id
            return 'changed'


def delete_manager(e_id):
    with get_session() as s:
        event = s.query(Event).get(e_id)
        if not event or event.status == 'deleted':
            abort(404, 'No event with this id')

        manager = s.query(Participation).filter(
                Participation.e_id == e_id,
                Participation.participation_role == 'manager'
        ).one_or_none()
        if not manager:
            abort(409, 'Event has no manager')
        s.delete(manager)


def update_event(e_id, data):
    with get_session() as s:
        event = s.query(Event).get(e_id)
        if not event or event.status == 'deleted':
            abort(404, 'No event with this id')

        for arg in data.keys():
            getattr(event, arg)
            if arg in ['id', 'status', 'views']:
                abort(400, "Can't change this field(s)")
            if arg == 'start_date' or arg == 'end_date':
                sdate = data[arg].split('-')
                date_s = date(int(sdate[0]), int(sdate[1]), int(sdate[2]))
                setattr(event, arg, date_s)
            elif arg == 'start_time':
                start_time = data[arg].split(':')
                time_start = time(int(start_time[0]), int(start_time[1]), 0, 0)
                setattr(event, arg, time_start)
            else:
                setattr(event, arg, data[arg])


def delete_event(e_id):
    with get_session() as s:
        event = s.query(Event).get(e_id)
        if not event:
            abort(404, 'No event with this id')
        if event.status == 'deleted':
            abort(409, 'Event already deleted')
        event.status = 'deleted'
            

def check_participation(u_id, e_id):
    with get_session() as s:
        event = s.query(Event).get(e_id)
        if not event or event.status == 'deleted':
            abort(404, 'No event with this id')

        participation = s.query(Participation).filter(
                Participation.e_id == e_id,
                Participation.u_id == u_id
        ).one_or_none()
        if participation:
            return participation.participation_role
        else:
            return 'not joined'


def get_presenters(e_id):
    result = []
    with get_session() as s:
        event = s.query(Event).get(e_id)
        if not event or event.status == 'deleted':
            abort(404, 'No event with this id')
        users = s.query(User, Participation).filter(
                User.id == Participation.u_id,
                Participation.e_id == e_id,
                Participation.participation_role == 'presenter',
                Participation.report_status == 'approved'
        ).all()

        for user, participant in users:
            result.append({
                'name': user.name,
                'surname': user.surname,
                'report': participant.report,
                'presenter_description': participant.presenter_description,
                'report_description': participant.report_description
            })

    return result


def join_event(u_id, e_id, data):
    with get_session() as s:
        event = s.query(Event).get(e_id)
        if not event or event.status == 'deleted':
            abort(404, 'No event with this id')

        is_consists = s.query(Participation).filter(
                Participation.u_id == u_id,
                Participation.e_id == e_id
        ).one_or_none()

        if is_consists:
            abort(409, 'User has already joined this event as [{}]'.format(is_consists.participation_role))
        role = 'viewer'
        participation = Participation(e_id=e_id, u_id=u_id,
                                      participation_role='viewer')
        if data['role'] == 'presenter':
            role = 'presenter'
            participation.participation_role = role
            participation.presenter_description = data['presenter_description']
            participation.report_description = data['report_description']
            participation.report_status = 'unseen'
        s.add(participation)
        logging.info('User [id {}] joined event [id {}] as [{}]'.format(u_id,
                                                                        e_id,
                                                                        role))