from PyKCS11 import *
import os

def rsa_encrypt_file(Slot_ID, file, public_key):
    try:
        pkcs11 = PyKCS11Lib()
        file_root = os.environ.get("File_Path")
        input_file = str(file_root)+"/"+str(file)
        HSM_SO = os.environ.get("HSM_SO_FILE")
        pkcs11.load(HSM_SO)
        mechanism = Mechanism(PyKCS11.CKM_RSA_PKCS)

        slot = pkcs11.getSlotList()[Slot_ID]
        session = pkcs11.openSession(slot)
        objects = session.findObjects([(PyKCS11.CKA_CLASS, PyKCS11.CKO_PUBLIC_KEY)])
        for obj in objects:
            key_info = session.getAttributeValue(obj, [PyKCS11.CKA_LABEL, PyKCS11.CKA_ID])
            if key_info[0] == public_key:
                public_key_obj = obj
                break
        else:
            raise ValueError("Public key not found")

        with open(input_file, 'rb') as file:
            plaintext = file.read()

        ciphertext = session.encrypt(public_key_obj, plaintext, mechanism)
        ciphertext_bytes = bytes(ciphertext)
        output_file = input_file + ".enc"
        with open(output_file, 'wb') as file:
            file.write(ciphertext_bytes)
        session.closeSession()
        result = "RSA Encryption işlemi başarılı"
        return result
    except:
        result = "RSA Encryption işlemi başarısız"
        return result
def rsa_decrypt_file(Slot_ID, private_key_password, file, private_key):
    try:
        pkcs11 = PyKCS11Lib()
        HSM_SO = os.environ.get("HSM_SO_FILE")
        file_root = os.environ.get("File_Path")
        input_file = str(file_root)+"/"+str(file)
        pkcs11.load(HSM_SO)
        mechanism = Mechanism(PyKCS11.CKM_RSA_PKCS)
        slot = pkcs11.getSlotList()[Slot_ID]
        session = pkcs11.openSession(slot)
        session.login(private_key_password)
        objects = session.findObjects([(PyKCS11.CKA_CLASS, PyKCS11.CKO_PRIVATE_KEY)])
        for obj in objects:
            key_info = session.getAttributeValue(obj, [PyKCS11.CKA_LABEL, PyKCS11.CKA_ID])
            if key_info[0] == private_key:
                private_key_obj = obj
                break
        else:
            raise ValueError("Private key not found")
        with open(input_file, 'rb') as file:
            ciphertext_bytes = file.read()
        output_file = input_file[:-4]
        plaintext_bytes = session.decrypt(private_key_obj, list(ciphertext_bytes), mechanism)
        with open(output_file, 'wb') as file:
            file.write(bytes(plaintext_bytes))
        session.closeSession()
        result = "RSA Decryption işlemi başarılı"
        return result
    except:
        result = "RSA Encryption işlemi başarısız"
        return result
