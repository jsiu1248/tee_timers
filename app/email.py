from flask import current_app, render_template
from flask_mail import Message
from . import mail
from threading import Thread

# asynch so that send_email doesn't have to wait in order to send email
def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

# using Message to create an email object
def send_email(to, subject, template, **kwargs):
    # actual application instead of just the proxy
    app = current_app._get_current_object()
    msg = Message(
        subject=current_app.config['RAGTIME_MAIL_SUBJECT_PREFIX'] + subject,
        recipients=[to],
        sender=current_app.config['RAGTIME_MAIL_SENDER'])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    thread = Thread(target=send_async_email, args=[app, msg])
    thread.start()