import os
from pathlib import Path
from crontab import CronTab
import sys


try:
        ENV_FILE_=sys.argv[1]
        if not ENV_FILE_ :
                exit("file name required")
        path=Path(os.getcwd(),ENV_FILE_)
        with open(path,'w+') as f:
                len=(os.path.getsize(path))
                f.truncate(len)
        # RESPONSE("CronJob executed",path)
except Exception as f:
        
        pass
        # ERROR(".ENV file truncate operation failed",f)
 

#remove crontab itself
cron=CronTab(user=True)
cron.remove_all(comment="passman delete password file")
cron.write()
