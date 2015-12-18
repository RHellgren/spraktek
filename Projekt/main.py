# -*- coding: utf-8 -*-
import requests
import json
import pprint
import sys
import codecs
import random
import math
from timeit import default_timer as timer
from xml.dom import minidom

pp = pprint.PrettyPrinter(indent=4)

def number_of_ngrams(n):
  with codecs.open(str(n) + '-grams.txt','rb',encoding='utf-8', errors='ignore') as f:
    lines = f.readlines()
    s = 0
    for line in lines:
      tokens = line.split()
      s += int(tokens[n])

    return s

unigram_count = number_of_ngrams(1)
bigram_count = number_of_ngrams(2)

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
  return [translate_word(word, lang_from, lang_to) for word in sentence.split()]

def translate_with_1gram(translated_words):
  translation = []
  sentence_score = 0
  for words in translated_words:
    best_score = -math.inf
    best_word = None
    for word in words:
      score = unigram_prob(word)
      if(score > best_score):
        best_word = word
        best_score = score

    if(best_score > -math.inf):
      sentence_score += best_score
    elif(best_word == None):
      best_word = random.choice(words)
      pp.pprint("No unigrams found, randomly selecting \"" + best_word + "\"")
      pp.pprint(words)

    translation.append(best_word)

  return (sentence_score, list_to_str(translation))

def translate_with_2gram(translated_words):
  (score, translation) = viterbi(translated_words)
  return (score, list_to_str(translation))

def list_to_str(l):
  sentence = ""
  for word in l:
    sentence += word + " "
  return sentence.strip()

def translate_word(word, lang_from, lang_to):
  payload = {"word": word, "from": lang_from, "to": lang_to}
  translation = requests.get("http://localhost:8080", params=payload)

  if translation.status_code != requests.codes.ok:
    print(translation.text)
    translation.raise_for_status()

  json = translation.json()
  translations = json["translations"]
  return [elem for elem in translations if " " not in elem]   

def viterbi(translations):
  V = [{}]
  path = {}
  min_prob = math.log(math.pow(10, -100))

  for y in translations[0]:
    V[0][y] = unigram_prob(y)
    path[y] = [y]

  for t in range(1, len(translations)):
    V.append({})
    newpath = {}

    for word in translations[t]:
      best_word = None
      best_score = -math.inf

      for prev_word in translations[t-1]:
        u = unigram_prob(word)
        b = bigram_prob(prev_word, word)

        # it's very improbable, but it might be our data that is wrong
        if(u == -math.inf):
          u = min_prob
        if(b == -math.inf):
          b = min_prob
        
        word_score = V[t-1][prev_word] + u + b

        if(word_score > best_score):
          best_word = prev_word
          best_score = word_score

      if(best_word == None):
        best_word = random.choice(translations[t-1])

      V[t][word] = best_score
      newpath[word] = path[best_word] + [word]

    path = newpath

  n = len(translations) - 1
  (score, state) = max((V[n][y], y) for y in translations[n])

  return (score, path[state])

def find_first_index(word, index_file):
  with codecs.open(index_file,'rb',encoding='utf-8') as f:
    for line in f:
      if word[:2] == line[:2]:
        break
  info = line.split()
  return int(float(info[1]))

def unigram_prob(word):
  with codecs.open('1-grams.txt','rb',encoding='utf-8', errors='ignore') as f:
    index = find_first_index(word, '1-gram-index.txt')
    if(index < 0):
      return -math.inf

    while True:
      f.seek(index)
      line = f.readline()
      tokens = line.split()

      if(line[:2] != word[:2]):
        return -math.inf

      if(tokens[0] == word):
        return math.log(int(tokens[1]) / unigram_count)

      index += len(line.encode('utf-8'))

def bigram_prob(word1, word2):
  bigrams = find_word_bigrams(word1)
  for bigram in bigrams:
    if(bigram['word'] == word2):
      return math.log(bigram['score'] / bigram_count)
  return -math.inf

def find_word_bigrams(word):
  list_of_bigrams = []
  with codecs.open('2-grams.txt','rb',encoding='utf-8', errors='ignore') as f:
    index = find_first_index(word, '2-gram-index.txt')
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
  bing_result = bing_translate_sentence(lang_from, lang_to, sentence)
  translated_words = tyda_translate_sentence(lang_from, lang_to, sentence)

  start = timer()
  translation_1gram = translate_with_1gram(translated_words)
  mid = timer()
  translation_2gram = translate_with_2gram(translated_words)
  end = timer()
  
  pp.pprint("Original sentence")
  pp.pprint(sentence)
  pp.pprint("Translating with 1-gram " + ("%.2f" % (mid-start)) + "s")
  pp.pprint(translation_1gram)
  pp.pprint("Translating with 2-gram " + ("%.2f" % (end-mid)) + "s")
  pp.pprint(translation_2gram)
  pp.pprint("Translating via Bing")
  pp.pprint(bing_result)

if __name__ == "__main__":
  l = len(sys.argv)
  if(l > 4):
    print("Passed too many arguments. Got", l, "expected 4")
  elif(l < 4):
    print("Passed too few arguments., Got", l, " expcted 4")
  else:
    main(sys.argv[1], sys.argv[2], sys.argv[3])
