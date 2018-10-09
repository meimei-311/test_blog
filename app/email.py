# coding=utf-8
from threading import Thread
from flask import current_app, render_template
from flask_mail import Message
from . import mail


def send_async_email(app, msg):
    with app.app_context():
        res = mail.send(msg)


def send_email(to, subject, template, **kwargs):
    app = current_app._get_current_object()
    msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + 'sss ' + subject,
                  sender=app.config['FLASKY_MAIL_SENDER'], recipients=[to])
    s = render_template(template + '.txt', **kwargs)
    s1 = render_template(template + '.html', **kwargs)
    s.encode('gbk')
    s1.encode('gbk')
    msg.body = s
    msg.html = s1
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr
