import requests
import json

with open('secrets.json') as data_file:    
    secrets = json.load(data_file)

headers = {"content-type": "application/x-www-form-urlencoded"}
payload = {"grant_type": "client_credentials", "client_id": secrets["client_id"], "client_secret": secrets["client_secret"], "scope": "http://api.microsofttranslator.com"}
#payload_str = "&".join("%s=%s" % (k,v) for k,v in payload.items())
auth = requests.post("https://datamarket.accesscontrol.windows.net/v2/OAuth2-13", data=payload, headers=headers)

if auth.status_code != requests.codes.ok:
  auth.raise_for_status()

token = auth.json()["access_token"]

print("Received token:", token)