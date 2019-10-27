import base64
import os
from communications import Communications
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import (
    Mail, Attachment, FileContent, FileName,
    FileType, Disposition, ContentId)
import sys


class EmailComms(Communications):

    def __init__(self,to,messagetype,mode,inpt,smtpsrvr,smtpcreds,frm,subject,apikey,summarybody,attachmentflag,loghndler):
        super().__init__(to,messagetype,mode,inpt)
        self.smtpsrvr=smtpsrvr
        self.smtpcreds=smtpcreds
        self.frm=frm
        self.subject=subject
        self.apikey=apikey
        self.summarybody=summarybody
        self.attachmentflag=attachmentflag
        self.loghndler=loghndler

    def sendsummaryemail(self):
        self.loghndler.info('Inside Summary email function..')
        email_body=self.html_template(self.summarybody,self.attachmentflag)
        # to_str=''
        # for str in self.to:
        self.loghndler.info('Successfully received summary body..')
        print(email_body['body'])
        if not self.attachmentflag=='Y':
            self.sendgrid_summary(email_body['body'])
            self.loghndler.info('Sent summary email without attachment...')
        else:
            # self.sendgrid_summary(email_body['body'])

            self.sendgrid_attachments(email_body)
            self.loghndler.info('Sent summary email with attachment...')

        

    def senderror(self):
        self.loghndler.info('Inside Error email function..')
        email_body=self.html_template('',self.attachmentflag)
        # to_str=''
        # for str in self.to:
        self.loghndler.info('Successfully received error body..')
        if self.attachmentflag=='Y':
            print(email_body['logfiles'])
            if len(email_body['logfiles'])>=1:
                self.sendgrid_attachments(email_body)
                self.loghndler.info('Sent error email with attachment...')
            else:
                print('No logs')
                self.loghndler.info('No error logs found...')
        else:
            if len(email_body['logfiles'])>=1:
                self.sendgrid_summary(email_body['body'])
                self.loghndler.info('Sent error email without attachment...')
            else:
                print('No logs')
                self.loghndler.info('No error logs found...')
        

    def sendemail(self):
        if self.messagetype=='both':
            try:
                self.sendsummaryemail()
            except Exception as e:
                print(f'Error in sending summary.Error:{e}')
                self.loghndler.error(f'Error in sending summary.Error:{e}',exc_info=True)
                sys.exit()
        elif self.messagetype=='error':
            try:
                self.senderror()
            except Exception as e:
                print(f'Error in sending error email.Error:{e}')
                self.loghndler.error(f'Error in sending error email.Error:{e}',exc_info=True)
                sys.exit()


    def sendgrid_summary(self,body):
        to_emails=self.transform_to_emails()
        
        message = Mail(
            from_email=('<email_change>', '<name_change>'),
            to_emails=to_emails,
            subject=self.subject,
            html_content=body)
        try:
            sendgrid_client = SendGridAPIClient(self.apikey)
            response = sendgrid_client.send(message)
            print(response.status_code)
            print(response.body)
            print(response.headers)
        except Exception as e:
            print(e)

    def sendgrid_attachments(self,bodyobj):
        to_emails=self.transform_to_emails()
        message = Mail(
            from_email=('<email_change>', '<name_change>'),
            to_emails=to_emails,
            subject=self.subject,
            html_content=bodyobj['body'])

        # attachments
        attchments=[]
        for fle in bodyobj['logfiles']:
            if fle=='None':
                continue
            else:

                with open(fle,'rb') as f:
                    dta=f.read()
                    fname=os.path.basename(f.name)
                encoded = base64.b64encode(dta).decode()
                attachment = Attachment()
                attachment.file_content = FileContent(encoded)
                # text/plain text/comma-separated-values
                attachment.file_type = FileType('text/plain')
                attachment.file_name = FileName(fname)
                attachment.disposition = Disposition('attachment')
                attachment.content_id = ContentId('Example Content ID')
                attchments.append(attachment)
        message.attachment = attchments
        try:
            sendgrid_client = SendGridAPIClient(self.apikey)
            response = sendgrid_client.send(message)
            print(response.status_code)
            print(response.body)
            print(response.headers)
        except Exception as e:
            print(e)

    def transform_to_emails(self):
        emailstr=self.to.split(',')
        if len(emailstr)==1:
            return emailstr[0]
        else:
            return [(x,f'Rec{i}') for i,x in enumerate(emailstr)]





