import requests


def FileDownloads(URL, filename):
    response = requests.post(url, data={"filename": filename})

    if response.status_code == 200:
        with open(filename, 'wb') as file:
            file.write(response.content)
        print(f"File '{filename}' downloaded and saved.")
    else:
        print("File download failed with status code:", response.status_code)

url = "http://localhost:8000/download"
filename = "TopSecret.rar"  # The desired filename

FileDownloads(url, filename)