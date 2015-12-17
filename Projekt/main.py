# -*- coding: utf-8 -*-
import requests
import json
import pprint
import sys
import codecs
import random
from xml.dom import minidom

pp = pprint.PrettyPrinter(indent=4)

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
  translated_words = [translate_word(word, lang_from, lang_to) for word in sentence.split()]
  #translated_words = [['så','vad','var','vilket'],['existera','var'],['kär','förälskad'],['omogen','unge','ansvar']]

  (score, translation) = find_best_sentence(translated_words)
  sentence = ""
  for word in translation:
    sentence += word + " "
  sentence = sentence.strip()

  return (score, sentence)

def translate_word(word, lang_from, lang_to):
  payload = {"word": word, "from": lang_from, "to": lang_to}
  translation = requests.get("http://localhost:8080", params=payload)

  if translation.status_code != requests.codes.ok:
    print(translation.text)
    translation.raise_for_status()

  json = translation.json()
  translations = json["translations"]
  return [elem for elem in translations if " " not in elem] 

def find_best_sentence(translations):
  V = [{}]
  path = {}

  for y in translations[0]:
    V[0][y] = 0
    path[y] = [y]

  for t in range(1, len(translations)):
    V.append({})
    newpath = {}

    for word in translations[t]:
      best_word = ""
      best_score = 0

      for prev_word in translations[t-1]:
        word_score = V[t-1][prev_word]
        bigrams = find_word_bigrams(prev_word)
        for bigram in bigrams:
          if(bigram['word'] == word):
            word_score = word_score + bigram['score'] 

        if(word_score > best_score):
          best_word = prev_word
          best_score = word_score

      if(best_score == 0):
        best_word = random.choice(translations[t-1])
        pp.pprint("No score for \"" + word + "\", randomly selected previous word to be \"" + best_word + "\"")

      V[t][word] = best_score
      newpath[word] = path[best_word] + [word]

    path = newpath

  n = len(translations) - 1
  (score, state) = max((V[n][y], y) for y in translations[n])

  return (score, path[state])

def find_first_index(word):
  with codecs.open('index.txt','rb',encoding='utf-8') as f:
    for line in f:
      if word[:2] == line[:2]:
        break
  info = line.split()
  return int(float(info[1]))

def find_word_bigrams(word):
  list_of_bigrams = []
  with codecs.open('bigrams_clean.txt','rb',encoding='utf-8', errors='ignore') as f:
    index = find_first_index(word)
    if(index < 0):
      return []

    while True:
      f.seek(index)
      line = f.readline()

      if(line[:2] != word[:2]):
        return list_of_bigrams

      tokens = line.split()
      if(tokens[0] == word):
        list_of_bigrams.append({'word': tokens[1], 'score': float(tokens[2])})
      
      index += len(line.encode('utf-8'))

  return []

def main(lang_from, lang_to, sentence):
#  bing_result = bing_translate_sentence(lang_from, lang_to, sentence)
  tyda_result = tyda_translate_sentence(lang_from, lang_to, sentence)
  
#  pp.pprint("Translating via Bing")
#  pp.pprint(bing_result)
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
