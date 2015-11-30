import requests
import json
import xml.etree.ElementTree

with open('secrets.json') as data_file:    
    secrets = json.load(data_file)

headers = {"content-type": "application/x-www-form-urlencoded"}
payload = {"grant_type": "client_credentials", "client_id": secrets["client_id"], "client_secret": secrets["client_secret"], "scope": "http://api.microsofttranslator.com"}
auth = requests.post("https://datamarket.accesscontrol.windows.net/v2/OAuth2-13", data=payload, headers=headers)

if auth.status_code != requests.codes.ok:
  print(auth.text)
  auth.raise_for_status()

access_token = auth.json()["access_token"]
print("Succesfully received access token")

text = "Failure"
auth_token = "Bearer" + " " + access_token
payload = {"text": text, "from": "en", "to": "sv"}

translation = requests.get("http://api.microsofttranslator.com/v2/Http.svc/Translate", params=payload, headers={"Authorization": auth_token}, stream=True)

if translation.status_code != requests.codes.ok:
  print(translation.text)
  translation.raise_for_status()

output_file = "output.xml"
chunk_size = 10
with open(output_file, 'wb') as fd:
    for chunk in translation.iter_content(chunk_size):
        fd.write(chunk)
