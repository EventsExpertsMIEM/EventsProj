import random
import string
import smtplib
from email.message import EmailMessage
from .config import cfg
import logging


def random_string_digits(str_len=8):
    """Generate a random string of letters and digits """
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.SystemRandom().choice(letters_and_digits) for i in range(str_len))


# возможно переписать как отдельный модуль ибо каждый раз логин+анлогин хз
def send_email(email, link):
    server = smtplib.SMTP_SSL(cfg.SMTP_HOST, 465)
    server.login(cfg.MAIL_LOGIN, cfg.MAIL_PASSWORD)
    message = cfg.SITE_ADDR + "/confirm/" + link

    msg = EmailMessage()
    msg.set_content(message)
    msg['Subject'] = "Your confirmation link"
    msg['From'] = cfg.MAIL_LOGIN
    msg['To'] = email
    server.send_message(msg)
    server.quit()


def send_reset_email(email, new_password):
    server = smtplib.SMTP_SSL(cfg.SMTP_HOST, 465)
    server.login(cfg.MAIL_LOGIN, cfg.MAIL_PASSWORD)
    message = 'Your new password - ' + new_password 

    msg = EmailMessage()
    msg.set_content(message)
    msg['Subject'] = "Your new password link"
    msg['From'] = cfg.MAIL_LOGIN
    msg['To'] = email
    server.send_message(msg)
    server.quit()


def send_500_email(e, err):
    server = smtplib.SMTP_SSL(cfg.SMTP_HOST, 465)
    server.login(cfg.MAIL_LOGIN, cfg.MAIL_PASSWORD)
    message = err

    msg = EmailMessage()
    msg.set_content(message)
    msg['Subject'] = "500 server error"
    msg['From'] = cfg.MAIL_LOGIN
    msg['To'] = cfg.SUPER_ADMIN_MAIL
    server.send_message(msg)
    server.quit()
