import requests
import json

def AESEncrypt(url, ID, PIN, init_vec,KName,file_Name):
    data = {
        "ID": ID,
        "PIN": PIN,
        "init_vector": init_vec,
        "KName": KName,
        "FNamePath": file_Name
    }

    headers = {'Content-Type': 'application/json'}

    response = requests.post(url, data=json.dumps(data), headers=headers)

    # Process the response as needed
    if response.status_code == 200:
        print("POST request successful.")
    else:
        print("POST request failed with status code:", response.status_code)

url = "http://127.0.0.1:8000/FileEncPYHSM/"
ID = 0
PIN = "1111"
init_vec = "2r4AlGJ7VsFS0AS1Dw4FCA=="
KName = "aes_key"
file_Name = "dene.txt"
AESEncrypt(url, ID, PIN, init_vec,KName,file_Name)