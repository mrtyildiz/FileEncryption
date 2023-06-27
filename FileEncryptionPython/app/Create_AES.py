from pyhsm.hsmclient import HsmClient
from pyhsm.hsmenums import HsmSymKeyGen

def AES_Create(Slot_ID,Slot_PIN,KeyName):
   with HsmClient(slot=Slot_ID, pin=Slot_PIN, pkcs11_lib="/lib64/libprocryptoki.so") as c:
     key_handle = c.create_secret_key(key_label=KeyName,
                                      key_type=HsmSymKeyGen.AES,
                                      key_size_in_bits=256,
                                      token=True,
                                      private=True,
                                      modifiable=False,
                                      extractable=False,
                                      sign=True,
                                      verify=True,
                                      decrypt=True,
                                      wrap=True,
                                      unwrap=True,
                                      derive=False)
     return key_handle