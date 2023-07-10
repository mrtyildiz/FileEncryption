import requests
import json

def RSADecrypt(url, ID, PIN,PrivName,file_Name):
    data = {
        "ID": ID,
        "PIN": PIN,
        "FileEncName": file_Name,
        "PrivateKeyName": PrivName
    }

    headers = {'Content-Type': 'application/json'}

    response = requests.post(url, data=json.dumps(data), headers=headers)

    # Process the response as needed
    if response.status_code == 200:
        print("POST request successful.")
    else:
        print("POST request failed with status code:", response.status_code)

url = "http://127.0.0.1:8000/RSAFileDec"
ID = 0
PIN = "1111"
PrivName = "private"
file_Name = "TopSecret.rar.enc"
RSADecrypt(url, ID, PIN,PrivName,file_Name)