from logfile import LogFile
import pandas as pd

class TextLog(LogFile):

    def __init__(self,logtype,logpath,keywords):
        super().__init__(logtype,logpath,keywords)
        self.logs={}

    def identify_errors(self):
        log_df=pd.DataFrame(columns=["process","logpath","status"])
        for apps,logpaths in self.logs.items():

            if len(logpaths)==0:
                log_df=log_df.append({"process":apps,"logpath":"None","status":"nologs"},ignore_index=True)
            else:
                for files in logpaths:
                    err=False
                    with open(files,'r') as filelines:
                        for lne in filelines:
                            if self.check_keywords(lne):
                                err=True
                                log_df=log_df.append({"process":apps,"logpath":files,"status":"e"},ignore_index=True)
                                break
                    if not err:
                        log_df=log_df.append({"process":apps,"logpath":files,"status":"s"},ignore_index=True)

                # log_df=log_df.append({"process":apps,"logpath":files,"status":"p"},ignore_index=True)

        return log_df


