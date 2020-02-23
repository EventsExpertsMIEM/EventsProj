from .config import cfg
from .db import *
from . import util
from . import logger
from .exceptions import (NotJsonError, NoData, ConfirmationLinkError
                         WrongDataError, WrongIdError)

from sqlalchemy.exc import IntegrityError
from sqlalchemy import desc

from datetime import datetime
import requests
import os
import nanoid


def get_user_info(user_id):
    with get_session() as s:
        user = s.query(User).get(user_id)
        if not user:
            raise WrongIdError('No user with this id')
        return {
            "mail": user.mail,
            "name": user.name,
            "surname": user.surname,
            "service_status": user.service_status,
            "phone": user.phone,
            "organization": user.organization,
            "position": user.position,
            "country": user.country,
            "bio": user.bio
        }


def get_user_events_by_role(user_id, role, offset, size):
    result = []
    with get_session() as s:
        user = s.query(User).get(user_id)
        if not user:
            raise WrongIdError('No user with this id')

        events = s.query(Participation, Event).filter(
                Participation.event == Event.id,
                Participation.participant == user_id,
                Participation.participation_role == role
        ).order_by(desc(Event.start_date))

        if offset and size:
            offset = int(offset)
            size = int(size)
            if offset < 0 or size < 1:
                raise WrongDataError('Offset or size has wrong values!')
            events = events.slice(offset, offset+size)
        elif not offset and not size:
            events = events.all()
        else:
            raise KeyError('Wrong query string arg.')

        for participant, event in events:
            result.append({
                'id': event.id,
                'name': event.name,
                'start_date': event.start_date
            })
    return result


def update_profile(user_id, data):
    with get_session() as s:
        user = s.query(User).filter(
                User.id == user_id,
                User.account_status == 'active',
        ).one_or_none()

        if user:
            for arg in data.keys():
                getattr(user, arg)
            for arg in data.keys():
                setattr(user, arg, data[arg])
        else:
            raise WrongIdError('No user with this id')


# админка

def get_users(offset, size):
    result = []
    with get_session() as s:
        users = s.query(User)
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
        for user in users:
            result.append({
                'id': user.id,
                'mail': user.mail,
                'name': user.name,
                'surname': user.surname,
                'service_status': user.service_status,
                'account_status': user.account_status
            })
    return result
