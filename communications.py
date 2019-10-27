import base64


class Communications:

    def __init__(self,to,messagetype,mode,inpt):
        self.to=to
        self.messagetype=messagetype ## summary or both
        self.mode=mode
        self.input=inpt

    def html_template(self,body,attchflg):
        input_df=self.input.copy()
        header_static={}
        logrow=[]
        tmplatetxt=''
        with open('message_templates/message_header.html','r') as tmplate:
            tmplatetxt=tmplate.read()

        if self.mode=='email':
            if body!='':
                header_static['body']=tmplatetxt
                    
                for row in input_df.index.tolist():
                    trow=f'<tr><td>{input_df.iloc[row]["process"]}</td><td>{self.translate_status(input_df.iloc[row]["status"])}</td><td>{input_df.iloc[row]["logpath"]}</td></tr>'
                    header_static['body']+=trow
                    if attchflg=='Y':
                        logrow.append(input_df.iloc[row]["logpath"])
                header_static['logfiles']=logrow



                footer_static='</table>\
                      </body>\
                      </html>'
                header_static['body']+=footer_static
            else:
                header_static['body']='<!DocType HTML>\
                    <html>\
                    <head>\
                    <style>\
                    </style>\
                    </head>\
                    <body>\
                    </body>\
                      </html>'

                for row in input_df.index.tolist():
                    if input_df.iloc[row]["status"]=='e':
                        logrow.append(input_df.iloc[row]["logpath"])
                header_static['logfiles']=logrow




        return header_static

        #--test html
        # with open('test.html','w') as fle:
        #     fle.write(header_static)

    @staticmethod
    def translate_status(statusval):
        translate_dict={'s':'SUCCESS','e':'ERROR','nologs':'NO LOGS FOUND'}
        return translate_dict[statusval]

    @staticmethod
    def read_log_content(logpath,encoding):
        lg=None
        with open(logpath,'r') as logfle:
            lg=logfle.read()

        if encoding=='base64':
            return base64.b64encode(lg)
        # encoded = base64.b64encode(data)
        # encoded = base64.b64encode(data).decode()


