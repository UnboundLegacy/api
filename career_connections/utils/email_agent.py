import re
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from flask import render_template, g

TITLE_PATTERN = re.compile(r'<title>(?P<title>.*)</title>')


class Message():
    '''
    Base Class for a generic email
    '''

    def __init__(self, sender, recipients, template, context):
        self.sender = sender
        self.recipients = recipients
        self.template = template
        self.ctx = context

        self.ctx['web_app_base'] = 'localhost:5000'

    def render_message(self):
        '''Render the email using Flask's Jinja2 environment'''
        body = render_template(self.template, **self.ctx)
        msg = MIMEText(body, 'html')
        msg['Subject'] = self.get_title(body)
        msg['From'] = self.sender
        msg['To'] = self.recipients
        # msg.attach(MIMEText(body, 'html'))
        return msg.as_string()

    def get_title(self, body):
        match = re.search(TITLE_PATTERN, body)
        if not match:
            return 'Unbound Legacy'
        return match.groupdict().get('title', 'Unbound Legacy')


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
        self.server.sendmail(message.sender, message.recipients, message.render_message())


class GmailAgent(BaseEmailAgent):
    '''
    An email agent for sending emails via Gmail
    '''
    host = 'smtp.gmail.com'
