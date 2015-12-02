# -*- coding: utf-8 -*-
import requests
import json
import pprint
import sys
import codecs
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
  translated_sentence = itemlist[0].firstChild.nodeValue

  return translated_sentence

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

def find_first_index(word):
  with codecs.open('index.txt','r',encoding='utf8') as f:
    for line in f:
      if word[:2] == line[:2]:
        break
  info = line.split()
  return info[1]

def find_word_info(word):
  list_of_bigrams = []
  with codecs.open('bigrams_clean.txt','r',encoding='utf8') as f:
    index = find_first_index(word)
    f.seek(index)
    line = f.readline()
    while line[:2] == word[:2]:
      list_of_bigrams.append(line.split())
      index += len(line)
  return list_of_bigrams

def main(lang_from, lang_to, sentence):
  bing_result = bing_translate_sentence(lang_from, lang_to, sentence)
  tyda_result = tyda_translate_sentence(lang_from, lang_to, sentence)
  
  pp = pprint.PrettyPrinter(indent=4)
  pp.pprint("Translating via Bing")
  pp.pprint(bing_result)
  pp.pprint("Translating via Tyda")
  pp.pprint(tyda_result)

if __name__ == "__main__":
  l = len(sys.argv)
  if(l > 4):
    print("Passed too many arguments. Got", l, "expected 4")
  elif(l < 4):
    print("Passed too few arguments., Got", l, " expcted 4")
  else:
    main(sys.argv[1], sys.argv[2], sys.argv[3])