from .config import cfg
from .db import *
from . import util
from .exceptions import (NotJsonError, NoData, WrongIdError)

from sqlalchemy.exc import IntegrityError
from sqlalchemy import desc, or_

from datetime import date, time
import requests
import logging
import os
import nanoid


def get_event_info(event_id):
    with get_session() as s:
        event = s.query(Event, Participation, User).filter(
                Event.id == event_id,
                Participation.event == Event.id,
                Participation.participant == User.id,
                Participation.participation_role == 'creator'
        ).first()

        if not event:
            raise WrongIdError('No event with this id')

        return {
            "creator_mail": event.User.mail,
            "phone": event.User.phone,
            "name": event.Event.name,
            "sm_description": event.Event.sm_description,
            "description": event.Event.description,
            "start_date": event.Event.start_date,
            "end_date": event.Event.end_date,
            "start_time": event.Event.start_time,
            "location": event.Event.location,
            "site_link": event.Event.site_link,
            "additional_info": event.Event.additional_info
        }


def get_events(offset, size):
    result = []
    with get_session() as s:
        events = s.query(Event).order_by(desc(Event.start_date))
        if offset and size:
            offset = int(offset)
            size = int(size)
            if offset < 0 or size < 1:
                raise WrongDataError('Offset or size has wrong values')
            events = events.slice(offset, offset+size)
        elif not offset and not size:
            events = events.all()
        else:
            raise KeyError('Wrong query string arg.')

        for event in events:
            result.append({
                'id': event.id,
                'name': event.name,
                'sm_description': event.sm_description,
                'start_date': event.start_date,
                'end_date': event.end_date,
                'start_time': event.start_time,
                'location': event.location,
                'site_link': event.site_link
            })
    return result


def create_event(user_id, data):
    start_date = data['start_date'].split('-')
    date_start = date(int(start_date[0]), int(start_date[1]), int(start_date[2]))

    date_end = None
    start_time = None
    if 'end_date' in data.keys():
        end_date = data['end_date'].split('-')
        date_end = date(int(end_date[0]), int(end_date[1]), int(end_date[2]))
    if 'start_time' in data.keys():
        start_time = data['start_time'].split(':')
        time_start = time(int(start_time[0]), int(start_time[1]), 0, 0)
    
    with get_session() as s:
        event = Event(name=data['name'], sm_description=data['sm_description'],
                      description=data['description'], start_date=date_start,
                      end_date=date_end, start_time=time_start,
                      location=data['location'], site_link=data['site_link'],
                      additional_info=data['additional_info'])
        s.add(event)
        s.flush()
        s.refresh(event)
        participation = Participation(event=event.id, participant=user_id,
                                      participation_role='creator')

        logging.info('Creating event [{}] [{}] [{}] [{}]'.format(data['name'],
                                                                 date_start,
                                                                 date_end,
                                                                 start_time))
        return event.id


def update_event(user_id, event_id, data):
    with get_session() as s:
        event = s.query(User, Event, Participation).filter(
                User.id == user_id,
                Event.id == event_id,
                Participation.event == Event.id,
                Participation.participant == User.id,
                or_(Participation.participation_role == 'creator',
                    User.service_status == 'admin',
                    User.service_status == 'moderator')
                User.account_status == 'active',
        ).one_or_none()
        ????????????????????????????????????????????????????????????????????????????
        for arg in data.keys():
            getattr(user, arg)
        for arg in data.keys():
            setattr(user, arg, data[arg])


# old functions

def check_participation(user_id, event_id):
    with get_session() as s:
        participation = s.query(Participation).filter(
                Participation.event == event_id,
                Participation.participant == user_id
        ).one_or_none()
        if participation:
            return participation.participation_role
        else:
            return 'not joined'


def get_presenters(id):
    result = {}
    with get_session() as s:
        users = s.query(User, Participation).filter(
                User.id == Participation.participant,
                Participation.event == id,
                Participation.participation_role == 'presenter' 
        ).all()

        i = 1
        for user, participant in users:
            result[i] = {
                'name': user.name,
                'surname': user.surname,
                'participation_role': participant.participation_role,
            }
            i += 1

    return result


def join_event(user_id, event_id, role):
    with get_session() as s:
        is_consists = s.query(Participation).filter(
                Participation.participant == user_id,
                Participation.event == event_id
        ).one_or_none()

        if not is_consists:
            participation = Participation(event=event_id, participant=user_id,
                                          participation_role=role)
            s.add(participation)
            logging.info('User [id {}] joined event [id {}] as [{}]'.format(user_id,
                                                                    event_id,
                                                                    role))
            return 0
        else:
            return 'User has already joined this event'


def event_exist(event_id):
    with get_session() as s:
        exists = s.query(Event).filter(
                Event.id == event_id
        ).count()
    return True if exists > 0 else False


def event_info(id):
    with get_session() as s:
        event = s.query(Event, Participation, User).filter(
                Event.id == id,
                Participation.event == Event.id,
                Participation.participant == User.id,
                Participation.participation_role == 'creator'
        ).first()

        return {
            "creator_mail": event.User.mail,
            "phone": event.User.phone,
            "name": event.Event.name,
            "sm_description": event.Event.sm_description,
            "description": event.Event.description,
            "start_date": event.Event.start_date,
            "end_date": event.Event.end_date,
            "start_time": event.Event.start_time,
            "location": event.Event.location,
            "site_link": event.Event.site_link,
            "additional_info": event.Event.additional_info
        }





# TODO TODO




def update_event(user_id, event_id, params):
    with get_session() as s:
        event = s.query(Participation, Event).filter(
                Event.id == id,
                Participation.event == Event.id,
                Participation.participant == user_id,
                Participation.participation_role.in_(['creator', 'manager'])
        ).one_or_none()

        if event is None:
            return "You have no rights to edit this event"
        else:
            ev = event.Event

            try:
                print(ev['name'])
            except Exception as e:
                print(e)

            return "Updated successfully"
