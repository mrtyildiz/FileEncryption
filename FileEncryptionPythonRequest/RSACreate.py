import requests
import json

def RSACreate(url, ID, PIN, PubKeyName,PrivKeyName):
    data = {
        "ID": ID,
        "PIN": PIN,
        "PublicLabel": PubKeyName,
        "PrivateLabel": PrivKeyName
    }

    headers = {'Content-Type': 'application/json'}

    response = requests.post(url, data=json.dumps(data), headers=headers)

    # Process the response as needed
    if response.status_code == 200:
        print("POST request successful.")
    else:
        print("POST request failed with status code:", response.status_code)

url = "http://127.0.0.1:8000/RSACreate/"
ID = 0
PIN = "1111"
PubKeyName = "publicdene"
PrivKeyName = "privdene"
RSACreate(url, ID, PIN, PubKeyName,PrivKeyName)