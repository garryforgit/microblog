#coding=utf-8

from flask.ext.mail import Message
from app import mail
from flask import ADMINS
from flask import render_template
def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    mail.send(msg)

def follower_notification(followed, follower):
    send_email("[microblog] %s now following you!" % follower.nickname, ADMINS[0]
               [followed.email],
               render_template("follower_email.txt",
                               user=followed, follower=follower),
               render_template("follower_email.html",
                               user=followed, follower=follower))

