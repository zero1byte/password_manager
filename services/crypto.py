from Crypto.PublicKey import RSA
import os,sys
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Util.Padding import pad, unpad
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64
from Crypto.Protocol.KDF import PBKDF2

from services import ERROR,RESPONSE,file
from config import PRIVATE_KEY_FILE,PUBLIC_KEY_FILE

class Asymmentric:
    directory=False
    pwd=False

    def __init__(self,dir=""):
        self.pwd=os.getcwd()
        self.private_key_str=None
        self.public_key_str=None
        if(not dir):
            self.directory=self.pwd
        else:
            self.directory=dir
        self.f=file(False,self.directory)

    def store_keys(self, key_size=2048):
        key = RSA.generate(key_size)
        #private key
        private_key=key.export_key('PEM').decode("utf-8")
        self.f.create(PRIVATE_KEY_FILE)
        self.f.write(PRIVATE_KEY_FILE, private_key)
        #public key generate & store
        public_key = key.publickey()
        public_key=public_key.export_key('PEM').decode("utf-8")
        self.f.create(PUBLIC_KEY_FILE)
        self.f.write(PUBLIC_KEY_FILE, public_key)
        return True
    
    def private_key(self):
        try:
            if not self.private_key_str:
                self.private_key_str = self.f.read(PRIVATE_KEY_FILE)
            return self.private_key_str
        except:
            ERROR("Private key not getting | try again")
            return False
        
    # if is store key is valid or not
    #@param - False : if private key is encrypted
    # else True
    def is_valid_private_key(self):
        try:
            private_key= self.private_key()
            RSA.import_key(private_key)
            return True
        except:
            ERROR("Private key not valid | try again")
            return False
        
    def is_valid_public_key(self):
        try:
            key= self.public_key()
            RSA.import_key(key)
            return True
        except:
            ERROR("Public key not valid | try again")
            return False
    
    def public_key(self):
        try:
            if not self.public_key_str:
                self.public_key_str= self.f.read(PUBLIC_KEY_FILE)
            return self.public_key_str
        except :
            ERROR("Public key not getting | try again")
            return False
    
    # RSA Encryption
    def en(self, string):
        try:
            public_key_data = self.f.read(PUBLIC_KEY_FILE)
            public_key = RSA.import_key(public_key_data)
            cipher = PKCS1_OAEP.new(public_key)
            # decode from bytes/binary into string
            encrypted = cipher.encrypt(string.encode())
            return (base64.b64encode(encrypted).decode())
        except Exception as e:
            ERROR(f"Encryption failed: {e}")
            return False

    # RSA Decryption 
    def de(self, encrypted_bytes):
        try:
            private_key_data = self.f.read(PRIVATE_KEY_FILE)
            private_key = RSA.import_key(private_key_data)
            cipher = PKCS1_OAEP.new(private_key)
            #encode from bytes into string
            decrypted = cipher.decrypt(base64.b64decode(encrypted_bytes.encode()))
            return decrypted.decode()
        except Exception as e:
            ERROR(f"Decryption failed: {e}")
            return False


# Encryption with AES
class Symmentric():
    def __init__(self, password):
        self.password = password  # This is a user-defined key string, not the AES key
        self.f=file(isJSON=False)
        self.asym=Asymmentric()

    def en(self, p_text):
        try:
            salt = get_random_bytes(16)
            key = PBKDF2(self.password, salt, dkLen=32)
            cipher = AES.new(key, AES.MODE_GCM)
            ciphertext, tag = cipher.encrypt_and_digest(pad(p_text.encode('utf-8'), AES.block_size))
            
            result = {
                "salt": base64.b64encode(salt).decode(),
                "nonce": base64.b64encode(cipher.nonce).decode(),
                "ciphertext": base64.b64encode(ciphertext).decode(),
                "tag": base64.b64encode(tag).decode()
            }
            RESPONSE(" encryption done ",None)
            return result
        except Exception as e:
            ERROR("Encryption failed:", e).print()
            exit
            return False

    def de(self, data):
        try:
            salt = base64.b64decode(data["salt"])
            nonce = base64.b64decode(data["nonce"])
            ciphertext = base64.b64decode(data["ciphertext"])
            tag = base64.b64decode(data["tag"])
            
            key = PBKDF2(self.password, salt, dkLen=32)
            cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
            p_text = cipher.decrypt_and_verify(ciphertext, tag)
            RESPONSE(" decryption done ",None)
            return unpad(p_text, AES.block_size).decode('utf-8')
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ERROR(f"Decryption failed: { e } ", f"({exc_type}, {fname}, {exc_tb.tb_lineno})").print()
            exit(0)
            return False
        

    def encrypt_keys(self):
        try:
            en_key= self.en(self.asym.private_key())
            self.f.write(PRIVATE_KEY_FILE,en_key)
            en_key_public= self.en(self.asym.public_key())
            self.f.write(PUBLIC_KEY_FILE,en_key_public)
        except Exception as e:
            ERROR("RSA keys not encrypt",e).print()
            exit
            return False
        
    def decrypt_keys(self):
        try:
            en_key=self.de(self.asym.private_key())
            self.f.write(PRIVATE_KEY_FILE,en_key)
            en_key_public=self.de(self.asym.public_key())
            self.f.write(PUBLIC_KEY_FILE,en_key_public)
        except Exception as e:
            ERROR("RSA keys not decrypt",e).print()
            return False

    def keyForm(self):
        # help to find what's the form of key
        # 1 : encrypted key
        # 2 : decrypted key
        # 0 : key not find
        try:
            asyn=Asymmentric()
            prkey=asyn.private_key()
            RESPONSE("finding key form ")
            if str(prkey).find("-----BEGIN")>0:
                return 1
            else :
                return 2
        except Exception as e:
            ERROR("Key form not found",e).print()
            return 0

