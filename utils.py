import base64


class Utils:

    def __init__(self,path,pathfile):
        self.path=path
        self.pathfile=pathfile

    def read_params(self):
        param_dict={}
        with open(self.path) as paramfile:
            tmpdata=paramfile.readlines()
            for val in tmpdata:
                param_dict[val.split('=')[0]]=val.split('=')[1].rstrip()
        return param_dict

    def read_paths(self):
        path_dict={}
        with open(self.pathfile) as pathfile:
            tmpdata=pathfile.readlines()
            for val in tmpdata:
                path_dict[val.split(',')[0]]=val.split(',')[1].rstrip()
        return path_dict

