from pathlib import Path
import os
from datetime import datetime,timedelta
from crontab import CronTab
import sys,os



from services import file,ERROR,RESPONSE
from config import ENV_FILE_

# handle user session with crontab
class session :
    def __init__(self) :
        self.f=file()
        self.session_file=Path(os.getcwd(),ENV_FILE_)
        self.password=None
        self.verified=False


    # delay : minutes
    def init(self,password,timeAfterDelete=5):
        if  self.get() :
            return
        try:
            #Take password and create 2 file
            # 1. Password Container file
            # 2. Crontab file which will help us to delete password file after some time
            #insert password into file
            with open(self.session_file,"w+") as f:
                    f.write(password)
                    self.password=password
                    f.close()
            #crontab file
            #  password  File to be deleted
            description="passman delete password file "
            command = f'{sys.executable} {Path(os.getcwd(),"services","cronjob.py")} {self.session_file}'
            # Calculate the time 5 minutes from now
            delete_time = datetime.now() + timedelta(minutes=timeAfterDelete)

            # Format the cron time as 'Minute Hour Day Month *'
            cron_time = delete_time.strftime('%M %H %d %m *')#(min hour day month weekday)
            cron =CronTab(user=True)
            job=cron.new(command=command,comment=description)
            job.setall(cron_time)
            cron.write()
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ERROR(f"Session init failed: { e } ", f"({exc_type}, {fname}, {exc_tb.tb_lineno})")
            return



    def get(self):
        try:
            if self.password :
                return self.password
            else :
                with open(self.session_file,"r") as f:
                    p=f.read()
                    self.password=p
                    RESPONSE("Password fetched from session file")
                    if p:
                        return p
                    else:
                        return 
        except Exception as f:
            ERROR("password not fetched from session file",f)
            return 
        
    def remove(self):
        try:
            self.password=None
            self.verified=False
            self.f.write(self.session_file,"")
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ERROR(f"Encryption failed: { e } ", f"({exc_type}, {fname}, {exc_tb.tb_lineno})")
            return