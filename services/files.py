import os
import json
from pathlib import Path


from services import RESPONSE,ERROR


class file:

    directory=""
    pwd=False

    def __init__(self,isJSON=True,dir=""):
        self.pwd=os.getcwd()
        if(not dir):
            self.directory=self.pwd
        else:
            self.directory=dir
        self.isJSON=isJSON

    def is_file_exists(self,path):
        
        #check for file exists or not
        if os.path.exists(path):
            return True
        return False

    def create(self,filename=""):

        if not file:
            utility.ERROR("pass file name as argument")
            return False
        #check for file exists
        path = Path(self.directory, filename)
        if self.is_file_exists(path) :
            ERROR("File already exists",path)
            return False
        # create file
        f=open(path,'x')
        if f:
            f.close()
            RESPONSE("File created successfully",path)
            return path
        else:
            ERROR("File creation failed | Try again",path).print()
            return False

    def read(self,file):

        #check for file exists
        path = Path(self.directory ,file)
        if not self.is_file_exists(path) :
            ERROR("File not exists",self.directory)
            return 
        #read data from file
        f = open(path, 'r')
        if f:
            arr = f.read()
            if not arr.strip():
                ERROR("file is empty", path)
                return []
            if self.isJSON :
                # Change from String to Object
                return json.loads(arr)
            else :
                return arr
        else :
            ERROR("file data can't be read",path)
            return


    def write(self,file,data):

        if not (file and data):
            ERROR("file & data arguments required",file)
            return False
        else :
            path=Path(self.directory,file)
            if not self.is_file_exists(path):
                ERROR("File not found",path)
            else :
                f=open(path,'w')
                # change from Objects to String
                # if self.isJSON : f.write(json.dumps(data))
                # else : f.write(f"{data}")
                f.write(f"{data}")
                f.close()
                return True
        return False


    def delete(self,file):

        if( not file ):
            ERROR("file argument required",file)
            return False
        path=Path(self.directory,file)
        if not self.is_file_exists(path):
            ERROR("File not found",path)
        else :
            os.remove(path)
            RESPONSE("file deleted ",path)
            return True
        return False

    

           