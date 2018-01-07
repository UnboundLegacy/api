import smtplib

from flask import render_template


class Message():
    '''
    Base Class for a generic email
    '''
    def __init__(self, sender, recipients, template, context):
        self.sender = sender
        self.recipients = recipients
        self.template = template
        self.ctx = context

    def render_template(self):
        '''Render the email using Flask's Jinja2 environment'''
        return render_template(self.template, **self.ctx)


class BaseEmailAgent():
    '''
    Base email agent
    '''

    host = ''
    port = 465

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.connect()


    def connect(self):
        '''Set up the server connection to be able to send emails'''
        self.server = smtplib.SMTP_SSL(self.host, self.port)
        self.server.ehlo()
        self.server.login(self.username, self.password)

    def send_message(self, message):
        '''
        Sends the given instance of the Message via the email agent

        Improve: make this asynchronous
        '''
        self.server.send_message(message.render_template(), message.sender, message.recipients)


class GmailAgent(BaseEmailAgent):
    '''
    An email agent for sending emails via Gmail
    '''
    host = 'smtp.gmail.com'
