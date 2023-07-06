from PyKCS11 import *
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Util.Padding import unpad
# HSM PKCS#11 kütüphanesinin yolu
pkcs11_lib = "/lib64/libprocryptoki.so"

# HSM slot numarası
slot = 0

# HSM PIN değeri
pin = "1111"

# Anahtar etiketi
key_label = "aes_key"

# Dosya şifreleme işlemi
def encrypt_file(input_file, output_file, key):
    cipher = AES.new(key, AES.MODE_CBC)

    with open(input_file, 'rb') as file:
        plaintext = file.read()

    ciphertext = cipher.encrypt(pad(plaintext, AES.block_size))

    with open(output_file, 'wb') as file:
        file.write(cipher.iv)
        file.write(ciphertext)

# Dosya şifresini çözme işlemi
def decrypt_file(input_file, output_file, key):
    with open(input_file, 'rb') as file:
        iv = file.read(16)
        ciphertext = file.read()

    cipher = AES.new(key, AES.MODE_CBC, iv)

    plaintext = cipher.decrypt(ciphertext)
    plaintext = unpad(plaintext, AES.block_size)

    with open(output_file, 'wb') as file:
        file.write(plaintext)

# PyKCS11 kullanarak anahtarı al
def get_key_from_hsm():
    pkcs11 = PyKCS11Lib()
    pkcs11.load(pkcs11_lib)
    session = pkcs11.openSession(slot, CKF_SERIAL_SESSION | CKF_RW_SESSION)
    session.login(pin)

    key_template = [
        (CKA_LABEL, key_label),
        (CKA_CLASS, CKO_SECRET_KEY),
        (CKA_KEY_TYPE, CKK_AES),
    ]

    objects = session.findObjects(key_template)
    #print(objects)
    for obj in objects:
        attributes = session.getAttributeValue(obj, [CKA_VALUE])
        print(attributes)
        if attributes:
            key = bytes(attributes[0])
            return key

    session.logout()
    pkcs11.close()

# Anahtarı HSM'den al
key = get_key_from_hsm()

# Dosyayı şifrele
input_file = "input.txt"
encrypted_file = "encrypted.bin"
#encrypt_file(input_file, encrypted_file, key)
decrypt_file(encrypted_file, input_file, key)
