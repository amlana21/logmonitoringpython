import base64
import os
import stat,time


class LogFile:

    def __init__(self,type,paths,keywords):
        self.type=type
        self.paths=paths
        self.keywords=keywords

    def list_files(self,duration):
        log_dict={}
        for apps in self.paths:
            file_list=[]
            for root, sub_folders, files in os.walk(self.paths[apps]):
                # print(root)
                for file in files:
                    utme=os.stat(os.path.join(root, file))[stat.ST_MTIME]
                    


                    curr_tme=time.time()
                    

                    diff=curr_tme-utme
                    
                    if int(diff)<=int(duration)*60:
                        file_list.append(self.paths[apps]+'\\'+file)

            log_dict[apps]=file_list
        return log_dict

    def check_keywords(self,line):
        keywords=self.keywords.split(',')
        key_list=filter(lambda x:x in line,keywords)
        for i,elem in enumerate(key_list):
            return True
            # i+=1
        # if i>0:


        return False




