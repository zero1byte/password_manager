import atexit
import datetime
from datetime import datetime
from pathlib import Path
import os

from config import ERROR_LOGS_FILE,APP_LOGS_FILE

APP_LOGS=[]
ERROR_LOGS=[]

class ERROR :
    def __init__(self,error="",data="",code=500,status=False):
        self.errormsg=error
        self.code=code
        self.status=status
        self.data=data
        self.timestamp=datetime.now()
        ERROR_LOGS.append(f"{self.timestamp}  \"{self.errormsg}\" \"{self.data}\" {self.status} {self.code}\n")

        

    def print(self):
        print("\033[31mError : ",self.errormsg," :: ",self.data,"\033[0m")




class RESPONSE :
    def __init__(self,msg="",data="",code=200,status=True):
        self.msg=msg
        self.data=data
        self.code=code
        self.status=status
        self.timestamp=datetime.now()
        APP_LOGS.append(f"{self.timestamp}  \"{self.msg}\" \"{self.data}\" {self.status} {self.code}\n")

    def print(self):
        print("\033[92mResponse : ",self.msg, " :: ",self.data,"\033[0m")







# Insert all log list into file whenever program end
def updateLogs():
    # insert error logs into log file
    path=Path(os.getcwd(),ERROR_LOGS_FILE)
    if not os.path.exists(ERROR_LOGS_FILE):
         with open(path,"x") as f:
              f.close()
    if len(ERROR_LOGS)>0:
        with open(path,"a") as f:
                for log in ERROR_LOGS:
                    f.write(log)
                f.close()
    #update app logs in file
    path=Path(os.getcwd(),APP_LOGS_FILE)
    if not os.path.exists(ERROR_LOGS_FILE):
         with open(path,"x") as f:
              f.close()
    if len(APP_LOGS)>0:
        with open(path,"a") as f:
                for log in APP_LOGS:
                    f.write(log)
                f.close()
    

atexit.register(updateLogs)