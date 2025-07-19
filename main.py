#!/usr/bin/env python3


import argparse
import atexit

from services import *
from  config import APP_CMD_NAME


DBMS=database()
s=session()

def add(args):
        domain=args.domain or args.d or None
        password=args.password or args.p or None
        remarks=args.remarks or args.r or None
        if not (domain and password):
                ERROR("Domain & Password value required !! ","At add")
                return False
        obj=Data(domain=domain,password=password,remarks=remarks)
        obj.encrypt()
        DBMS.insert(obj)
        
def all(args):
        for obj in DBMS.getAll():
                print(obj)

def search(args):
        identifier=args.identifier or args.i or None
        if(not identifier):
                ERROR("Search string required ")
        for obj in DBMS.search(identifier):
                print(obj)

def delete(args):
        identifier=args.identifier or args.i or None
        if(not identifier):
                ERROR("identifier string required ")

def verifyUser():
        #get user application password & unlock keys
        if not s.get():
                password=input("Enter your key : ")
                s.init(password=password)
                return password
        else:
                return s.get()

def isAuthorized():
        asym=Asymmentric()
        print(asym.is_valid_private_key())


def  init(args):

        password=args.password or args.p or None
        
        if not s.get():
                if not password: 
                        verifyUser()
                else :
                        s.init(password=password)
        asyn=Asymmentric()
        if not (asyn.is_valid_private_key() and asyn.is_valid_public_key()):
                                print("Creating RSA keys..\n")
                                asyn.store_keys()
                                
        # Encrypt Public and Private key
        syn=Symmentric(s.get())
        if(syn.keyForm()==2):
                syn.encrypt_keys()



# main function of application
def main():

        # if user verified then decrypt keys
        if verifyUser():
                syn=Symmentric(s.get())
                if  (syn.keyForm()==2):
                        syn.decrypt_keys()
                else:
                        ERROR("Something went wrong at verify").print()
                        exit(0)
        


        parser = argparse.ArgumentParser(prog=APP_CMD_NAME, description="My CLI Tool for Secure Password locally")
        subparsers = parser.add_subparsers(dest="command", required=True)

        # 'add' sub cmd for add sub cmd
        parser_add = subparsers.add_parser("add", help="Add new entity")
        #take arg
        parser_add.add_argument("domain", nargs="?", help="Domain name")
        parser_add.add_argument("password",  nargs="?",help="Password")
        parser_add.add_argument("remarks",nargs="?",  help="Remarks (Optional)")
        parser_add.add_argument("-d","--d",  help="Domain name")
        parser_add.add_argument("-p",  "--p",help="Password")
        parser_add.add_argument("-r",  "--r",required=False,help="Remarks")
        #set funtion
        parser_add.set_defaults(func=add)


        # 'all' : sub cmd
        parser_all=subparsers.add_parser("all",help="get all Stored Password")
        parser_all.set_defaults(func=all)

        # 'search'
        parser_search=subparsers.add_parser("search",help="Search in database")
        parser_search.add_argument("identifier",nargs="?",help="Sub String for search")
        parser_search.add_argument("-i",required=False,help="Sub String for search")
        parser_search.set_defaults(func=search)

        # 'init' : store key and initial setup
        parser_search=subparsers.add_parser("init",help="Initial setup")
        parser_search.add_argument("password",nargs="?",help="app password")
        parser_search.add_argument("-p",required=False,help="app password")
        parser_search.set_defaults(func=init)

        # Parse and dispatch
        args = parser.parse_args()
        #run set Function and pass arg
        args.func(args)


# encrypt before exit from application
def atexit_exe():
        sys=Symmentric(s.get())
        sys.encrypt_keys()
        DBMS.update()

# update storage file at end of program
atexit.register(atexit_exe)


if __name__ == "__main__":
        main()