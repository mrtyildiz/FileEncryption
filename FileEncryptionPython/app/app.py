from fastapi import FastAPI
from pydantic import BaseModel
from Create_AES import AES_Create
from fastapi import File, UploadFile
import shutil
import base64
from FileEncryptPYHSM import encrypt_file, decrypt_file

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

@app.post("/AESCreate/")
def AESCreate(data: AESKey):
    # Gelen verileri kullanarak kaydetme işlemini gerçekleştirin
    Slot_ID = data.ID
    Slot_PIN = data.PIN
    KeyName = data.KName
    handler = AES_Create(Slot_ID,Slot_PIN,KeyName)
    return {"Oluşturulan Anahtarın handler değeri": handler}

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
    Init_Vector_bytes = base64.b64decode(Init_Vector)
    KName = data.KName
    FNamePath = data.FNamePath
    result = encrypt_file(Slot_ID, Slot_PIN, FNamePath, KName, Init_Vector_bytes)
    return result

@app.post("/FileDecPYHSM")
def FileDecryption(data: FileUploadDec):
    Slot_ID = data.ID
    Slot_PIN = data.PIN
    Init_Vector = data.init_vector
    Init_Vector_bytes = base64.b64decode(Init_Vector)
    KName = data.KName
    FNamePath = data.ENamePath
    result = decrypt_file(Slot_ID, Slot_PIN, FNamePath, KName, Init_Vector_bytes)
    return result

###### Init Vector Bytes ############
# import os
# iv = os.urandom(16)
# encoded_iv = base64.b64encode(iv).decode("utf-8")
# decoded_iv = base64.b64decode(encoded_iv)
# encoded_iv = base64.b64encode(decoded_iv).decode("utf-8")
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
