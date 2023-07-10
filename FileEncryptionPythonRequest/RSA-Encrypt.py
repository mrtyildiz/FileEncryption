import requests
import json

def RSAEncrypt(url, ID, PIN,PublicName,file_Name):
    data = {
        "ID": ID,
        "PIN": PIN,
        "FileName": file_Name,
        "PublicKeyName": PublicName
    }

    headers = {'Content-Type': 'application/json'}

    response = requests.post(url, data=json.dumps(data), headers=headers)

    # Process the response as needed
    if response.status_code == 200:
        print("POST request successful.")
    else:
        print("POST request failed with status code:", response.status_code)

url = "http://127.0.0.1:8000/RSAFileEnc"
ID = 0
PIN = "1111"
PublicName = "public"
file_Name = "TopSecret.rar"
RSAEncrypt(url, ID, PIN,PublicName,file_Name)