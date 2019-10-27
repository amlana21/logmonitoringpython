import logging
import datetime

class LoggerClass:
    def __init__(self,loggername):
        self.loggername=loggername

    def get_logs(self):
        logger=logging.getLogger(self.loggername)
        logger.setLevel(logging.INFO)

        c_handler=logging.StreamHandler()
        nw=datetime.datetime.now()
        log_file_name=f'{nw.year}-{nw.month}-{nw.day}-{nw.hour}-{nw.minute}-{nw.second}'
        f_handler=logging.FileHandler(f'logs/{log_file_name}.log')
        c_handler.setLevel(logging.INFO)
        f_handler.setLevel(logging.ERROR)
        f_handler.setLevel(logging.INFO)

        c_format=logging.Formatter('%(name)s-%(levelname)s-%(message)s')
        f_format=logging.Formatter('%(asctime)s-%(name)s-%(levelname)s-%(message)s',datefmt='%m:%d:%y:%H:%M:%S')
        c_handler.setFormatter(c_format)
        f_handler.setFormatter(f_format)

        logger.addHandler(f_handler)
        logger.addHandler(c_handler)

        return logger
