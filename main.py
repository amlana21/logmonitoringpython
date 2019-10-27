from utils import Utils
from logfile import LogFile
from textlogfile import TextLog
from communications import Communications
from email_comm import EmailComms
import sys
from loggerclass import LoggerClass

def main():

    ##--------------------initialize logger-------------------------------##
    try:
        logclass=LoggerClass('mainlog')
        loghandler=logclass.get_logs()
    except Exception as e:
        print('error in getting logger')
        sys.exit()
    ##--------------------end initialize logger-------------------------------##
    loghandler.info('Start Program execution....')
    ##--------------------read input params and monitoring paths----------##
    try:
        loghandler.info('Start reading input params..')
        utilobj=Utils('resources/params.properties','resources/paths.csv')

        params=utilobj.read_params()

        paths=utilobj.read_paths()
        loghandler.info('End reading input params..')
    except Exception as e:
        print('Error in reading input params')
        loghandler.error('Error in reading input params')
        sys.exit()

    ##--------------------end read input params and monitoring paths----------##



    ##--------------------make list of log files to monitor------------------##
    try:
        ##---------------text log files
        loghandler.info('Start getting list of logs modified..')
        logobj=TextLog(params['logtype'],paths,params['keywords'])
        log_dict1=logobj.list_files(params['logmodifiedduration(minutes)'])
        logobj.logs=log_dict1
        loghandler.info('Start identifying status for each logs..')
        status_dict=logobj.identify_errors()
        print(status_dict)
        loghandler.info('End getting list of logs modified..')
    except Exception as e:
        print(f'Error in reading or listing of logs. Error:{e}')
        loghandler.error(f'Error in reading or listing of logs. Error:{e}',exc_info=True)
        sys.exit()
    ##--------------------endmake list of log files to monitor------------------##

    ##------------------------start communications-----------------##
    # comobj=Communications('a','b','c',status_dict)
    # comobj.html_template()
    loghandler.info('Start processing logs..')
    if(params['sendmode']=='Both') | (params['sendmode']=='Summary'):
        emailobj=None
        try:
            loghandler.info('Initializing email object for summary mode..')
            emailobj=EmailComms(params['emailaddress'],'both','email',status_dict,params['smtphost'],{'usr':params['smtpuser'],'pswrd':params['smtppwd']},params['from'],params['summarysubject'],params['sendgrid_api'],params['summarysubject'],params['sendattachments'],loghandler)
        except Exception as e:
            print(f'Error in initializing email object.Error:{e}')
            loghandler.error(f'Error in initializing email object.Error:{e}',exc_info=True)
            sys.exit()
        loghandler.info('Calling send email function for summary mode..')
        emailobj.sendemail()
    elif params['sendmode']=='Error':
        emailobj=None
        try:
            loghandler.info('Initializing email object for error mode..')
            emailobj=EmailComms(params['emailaddress'],'error','email',status_dict,params['smtphost'],{'usr':params['smtpuser'],'pswrd':params['smtppwd']},params['from'],params['subject'],params['sendgrid_api'],'',params['sendattachments'],loghandler)
        except Exception as e:
            print(f'Error in initializing email object.Error:{e}')
            loghandler.error(f'Error in initializing email object.Error:{e}',exc_info=True)
            sys.exit()
        loghandler.info('Calling send email function for error mode..')
        emailobj.sendemail()
    loghandler.info('End processing logs..')
    ##------------------------end communications------------------##
    loghandler.info('End Program execution....')

if __name__=='__main__':
    main()