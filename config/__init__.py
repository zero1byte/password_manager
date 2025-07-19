# Holds files Names & Directory
from  pathlib import Path

APP_NAME="passman (Secure Local Password Manager)"
APP_CMD_NAME="passman"

PUBLIC_KEY_FILE=Path("services","keys", "public_key.pem")
PRIVATE_KEY_FILE=Path("services","keys","private_key.pem")
STORAGE_FILE=Path("data","storage.json")
APP_LOGS_FILE=Path("logs","app.log")
ERROR_LOGS_FILE=Path("logs","error.log")
PASSWORD_FILE_=Path("temp","password.tmp")
ENV_FILE_=Path("config",".env")


__all__=["PUBLIC_KEY_FILE","PRIVATE_KEY_FILE","STORAGE_FILE","APP_LOGS_FILE","ERROR_LOGS_FILE","PASSWORD_FILE_","ENV_FILE_",]