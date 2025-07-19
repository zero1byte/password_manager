import datetime
import json
import uuid


from services import RESPONSE,ERROR,Asymmentric,file
from config import STORAGE_FILE

Storage = []

class Data:
    def __init__(self,domain,password,remarks=None,createdAt=None,updatedAt=None,isEnrypted=False,id=None):
        if not id : 
            self.id= str(uuid.uuid4()) 
        else:
            self.id= id

        self.domain=domain
        self.password=password
        self.remarks=remarks
        if not createdAt :
            self.createdAt=datetime.datetime.now().strftime("%d:%m:%Y %H:%M:%S")
        else :
            self.createdAt=createdAt

        if not updatedAt :
            self.updatedAt=datetime.datetime.now().strftime("%d:%m:%Y %H:%M:%S")
        else :
            self.updatedAt=updatedAt

        self.isEnrypted=isEnrypted


    def encrypt(self):
        try:
            en=Asymmentric()
            encrypted_text=en.en(self.password)
            self.password=encrypted_text
            self.isEnrypted=True
        except Exception as e:
            ERROR("Object can't encrypt",str(e)).print()

    def decrypt(self):
        try:
            en=Asymmentric()
            if self.isEnrypted:
                self.password=en.de(self.password)
                self.isEnrypted=False
        except Exception as e:
            ERROR("Already encrypted",str(e)).print()

    def __str__(self):
        return json.dumps(self.__dict__,indent=5,default=str)
    
    def to_object(self):
        return self.__dict__
    
    



class database:
    def __init__(self):
        global Storage
        self.f=file()
        if(len(Storage)<=0):
            if not self.f.is_file_exists(STORAGE_FILE):
                self.f.create(STORAGE_FILE)
            else : 
                # Object String to Data Object
                previous_data= self.f.read(STORAGE_FILE)
                if not previous_data:
                    return
                Storage = [Data(**entry) for entry in previous_data]

    def getAll(self):
        return Storage

    def insert(self,obj):
        Storage.append(obj)


    def update(self):
        try:
            global Storage
            json_formet=[obj.to_object() for obj in Storage]
            self.f.write(STORAGE_FILE,json.dumps(json_formet,indent=4))
            RESPONSE("Data updated at file",datetime.datetime.now().strftime("%d:%m:%Y %H:%M:%S"))
        except Exception as e:
            ERROR("Error while Updating Storage",str(e)).print()

    def search(self,identifier):
        try:
            searched=[]
            for obj in Storage:
                if f"{obj}".find(identifier)!=-1 :
                    searched.append(obj)
            return searched
        except Exception as e:
            ERROR("something wrong while search",str(e)).print()
            return []

    def delete(self,idetifier):
        try:
            for i,obj in enumerate(Storage):
                if f"{obj}".find(idetifier) != -1:
                    Storage.pop(i)
                    print(i,obj)
                    return True
            return False
        except Exception as e:
            ERROR("Something went wrong while delete",str(e)).print()
            return False

            






