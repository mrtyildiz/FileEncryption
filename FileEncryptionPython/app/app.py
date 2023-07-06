from fastapi import FastAPI
from pydantic import BaseModel
from Create_AES import AES_Create
from fastapi import File, UploadFile
import shutil
import base64
from FileEncryptPYHSM import encrypt_file, decrypt_file
from Create_RSA import RSACreate
from FileEncryptRSA import encrypt_file_rsa, decrypt_file_rsa
app = FastAPI()

class AESKey(BaseModel):
    ID: int
    PIN: str
    KName: str
class FileUploadEnc(BaseModel):
    ID: int
    PIN: str
    init_vector: str
    KName: str
    FNamePath: str

class FileUploadDec(BaseModel):
    ID: int
    PIN: str
    KName: str
    init_vector: bytes
    ENamePath: str

class RSAKey(BaseModel):
    ID: int
    PIN: str
    PublicLabel: str
    PrivateLabel: str

class FileEncryptRSA(BaseModel):
    ID: int
    PIN: str
    FileName: str
    PublicKeyName: str

class FileDecryptRSA(BaseModel):
    ID: int
    PIN: str
    FileEncName: str
    PrivateKeyName: str

@app.post("/AESCreate/")
def AESCreate(data: AESKey):
    # Gelen verileri kullanarak kaydetme işlemini gerçekleştirin
    Slot_ID = data.ID
    Slot_PIN = data.PIN
    KeyName = data.KName
    handler = AES_Create(Slot_ID,Slot_PIN,KeyName)
    return {"Oluşturulan Anahtarın handler değeri": handler}

@app.post("/RSACreate/")
def RSA_Create(data: RSAKey):
    Slot_ID = data.ID
    Slot_PIN = data.PIN
    PublicLabel = data.PublicLabel
    PrivateLabel = data.PrivateLabel
    result = RSACreate(Slot_ID,Slot_PIN,PublicLabel,PrivateLabel)
    return {result}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    file_destination = f"./{file.filename}"
    with open(file_destination, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    print("Yüklenen dosyanın adı:", file.filename)
    print("/app/"+file.filename)
    return {"message": "Dosya başarıyla yüklendi", "filename": file.filename}
@app.post("/FileEncPYHSM")
def FileEncryption(data: FileUploadEnc):
    Slot_ID = data.ID
    Slot_PIN = data.PIN
    Init_Vector = data.init_vector
    print(Init_Vector)
    Init_Vector_bytes = base64.b64decode(Init_Vector)
    print(Init_Vector_bytes)
#    Init_Vector_bytes2 = Init_Vector.encode()
 #   print(Init_Vector_bytes2)
  #  Init_Vector_bytes = b'\xdc\xb5S\x9b\x12hc\xd7\r60\xa5\xf8\xdc\xcbB'
    KName = data.KName
    FNamePath = data.FNamePath
    encrypt_file(Slot_ID, Slot_PIN, FNamePath, KName, Init_Vector_bytes)

@app.post("/FileDecPYHSM")
def FileDecryption(data: FileUploadDec):
    Slot_ID = data.ID
    Slot_PIN = data.PIN
    Init_Vector = data.init_vector
    Init_Vector_bytes = base64.b64decode(Init_Vector)
    KName = data.KName
    FNamePath = data.ENamePath
    decrypt_file(Slot_ID, Slot_PIN, FNamePath, KName, Init_Vector_bytes)

@app.post("/RSAFileEncrypt")
def RSA_File_Enc(data: FileEncryptRSA):
    Slot_ID = data.ID
    Slot_PIN = data.PIN
    File_Name = data.FileName
    PubName = data.PublicKeyName
    result = encrypt_file_rsa(Slot_ID, File_Name, PubName,Slot_PIN)
    return result

@app.post("/RSAFileDecrypt")
def RSA_File_Dec(data: FileDecryptRSA):
    Slot_ID = data.ID
    Slot_PIN = data.PIN
    File_Name = data.FileEncName
    PrivName = data.PrivateKeyName
    result = decrypt_file_rsa(Slot_ID, File_Name, PrivName, Slot_PIN)
    return result


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
