from PyKCS11 import *
from PyKCS11.LowLevel import CKA_CLASS, CKO_PUBLIC_KEY, CKA_LABEL, CKM_RSA_PKCS_OAEP, CKA_TOKEN, CKA_PRIVATE, CKA_MODULUS_BITS
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA

def encrypt_file_rsa(Slot_ID, file_path, public_key_label, pin):
    pkcs11_lib = '/lib64/libprocryptoki.so'
    output_path = file_path +".enc"
    lib = PyKCS11Lib()
    lib.load(pkcs11_lib)
    slot = lib.getSlotList(tokenPresent=True)[Slot_ID]
    session = lib.openSession(slot)
    session.login(pin)
    template = [
        (CKA_CLASS, CKO_PUBLIC_KEY),
        (CKA_LABEL, public_key_label)
    ]
    public_key = session.findObjects(template)[0]
    modulus = session.getAttributeValue(public_key, [CKA_MODULUS])[0]
    public_exponent = session.getAttributeValue(public_key, [CKA_PUBLIC_EXPONENT])[0]
    key = RSA.construct((int.from_bytes(modulus, byteorder='big'), int.from_bytes(public_exponent, byteorder='big')))
    cipher = PKCS1_OAEP.new(key)
    with open(file_path, 'rb') as file:
        file_data = file.read()
    encrypted_data = cipher.encrypt(file_data)
    with open(output_path, 'wb') as output_file:
        output_file.write(encrypted_data)
    session.logout()
    result = "File encrypted successfully"
    return result



def decrypt_file_rsa(Slot_ID, file_path, private_key_label, pin):
    pkcs11_lib = '/lib64/libprocryptoki.so'
    output_path = file_path[:-4]
    lib = PyKCS11Lib()
    lib.load(pkcs11_lib)
    slot = lib.getSlotList(tokenPresent=True)[Slot_ID]
    session = lib.openSession(slot)
    session.login(pin)
    template = [
        (CKA_CLASS, CKO_PRIVATE_KEY),
        (CKA_LABEL, private_key_label)
    ]
    private_key = session.findObjects(template)[0]
    modulus = session.getAttributeValue(private_key, [CKA_MODULUS])[0]
    public_exponent = session.getAttributeValue(private_key, [CKA_PUBLIC_EXPONENT])[0]
    private_exponent = session.getAttributeValue(private_key, [CKA_PRIVATE_EXPONENT])[0]
    key = RSA.construct((int.from_bytes(modulus, byteorder='big'), int.from_bytes(public_exponent, byteorder='big'), int.from_bytes(private_exponent, byteorder='big')))
    cipher = PKCS1_OAEP.new(key)
    with open(file_path, 'rb') as file:
        encrypted_data = file.read()
    decrypted_data = cipher.decrypt(encrypted_data)
    with open(output_path, 'wb') as output_file:
        output_file.write(decrypted_data)
    session.logout()
    result = "File decrypted successfully"
    return result
