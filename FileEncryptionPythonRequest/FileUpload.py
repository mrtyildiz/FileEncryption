import requests


def FileUpload(URL, FileName):

    with open(FileName, "rb") as file:
        response = requests.post(URL, files={"file": file})

    # Process the response as needed
url = "http://localhost:8000/upload"
file_path = "dene.txt"

FileUpload(url, file_path)