import random
import string
import smtplib
import logging
from flask_mail import Message
import app
from .config import cfg
import logging


def random_string_digits(str_len=8):
    """Generate a random string of letters and digits """
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.SystemRandom().choice(letters_and_digits) for i in range(str_len))


# возможно переписать как отдельный модуль ибо каждый раз логин+анлогин хз
def send_email(email, link):

    msg = Message(
        body = '{}"/confirm/"{}'.format(cfg.SITE_ADDR, link),
        subject = 'Congress Events confirmation link',
        recipients = [email],
    )

    logging.info('Sending confirmation message')

    app.mail.send(msg)

def send_reset_email(email, new_password):

    msg = Message(
        body = 'Your new password - '.format(new_password),
        subject = 'Congress Events password reset',
        recipients = [email]
    )

    logging.info('Sending password reset message')

    app.mail.send(msg)

def send_500_email(e, error):

    msg = Message(
        body = error,
        subject = 'Congress Events goes KA-BOOOM',
        recipients = [cfg.SUPER_ADMIN_MAIL],
    )

    logging.info('Sending 500 error message')

    app.mail.send(msg)
