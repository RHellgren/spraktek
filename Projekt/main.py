import requests
import json
import pprint
from xml.dom import minidom

def get_access_token():
  with open('secrets.json') as data_file:    
      secrets = json.load(data_file)

  headers = {"content-type": "application/x-www-form-urlencoded"}
  payload = {"grant_type": "client_credentials", "client_id": secrets["client_id"], "client_secret": secrets["client_secret"], "scope": "http://api.microsofttranslator.com"}
  auth = requests.post("https://datamarket.accesscontrol.windows.net/v2/OAuth2-13", data=payload, headers=headers)

  if auth.status_code != requests.codes.ok:
    print(auth.text)
    auth.raise_for_status()

  access_token = auth.json()["access_token"]

  return access_token

def bing_translate_sentence(lang_from, lang_to, sentence):
  access_token = get_access_token()
  payload = {"text": sentence, "from": lang_from, "to": lang_to}
  auth_token = "Bearer" + " " + access_token
  translation = requests.get("http://api.microsofttranslator.com/v2/Http.svc/Translate", params=payload, headers={"Authorization": auth_token}, stream=True)
  translation.encoding = "UTF-8"

  if translation.status_code != requests.codes.ok:
    print(translation.text)
    translation.raise_for_status()

  output_file = "output.xml"
  chunk_size = 10
  with open(output_file, 'wb') as fd:
      for chunk in translation.iter_content(chunk_size):
          fd.write(chunk)

  xmldoc = minidom.parse(output_file)
  itemlist = xmldoc.getElementsByTagName("string")
  return itemlist[0].firstChild.nodeValue

def tyda_translate_sentence(lang_from, lang_to, sentence):
  sentence_translations = []

  for word in sentence.split(" "):
    word_translations = translate_word(word, lang_from, lang_to)
    sentence_translations.append(word_translations)

  return sentence_translations

def translate_word(word, lang_from, lang_to):
  payload = {"word": word, "from": lang_from, "to": lang_to}
  translation = requests.get("http://localhost:8080", params=payload)

  if translation.status_code != requests.codes.ok:
    print(translation.text)
    translation.raise_for_status()

  json = translation.json()
  return json["translations"]

def main():
  sentence = "I fail at translating sentences"
  lang_from = "en"
  lang_to = "sv"

  bing_result = bing_translate_sentence(lang_from, lang_to, sentence)
  tyda_result = tyda_translate_sentence(lang_from, lang_to, sentence)
  
  pp = pprint.PrettyPrinter(indent=4)
  pp.pprint("Translating via Bing")
  pp.pprint(bing_result)
  pp.pprint("Translating via Tyda")
  pp.pprint(tyda_result)

if __name__ == "__main__":
  main()