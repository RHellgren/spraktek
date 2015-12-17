import codecs
from nltk import everygrams
import string
import sys
import re

def build(n, input_file, output_file_name):
  sentences = []
  with codecs.open(input_file,'r',encoding='utf8') as f:
     for line in f:
         sentences.append(line)

  ngrams = []
  exclude = set(string.punctuation)
  for sentence in sentences:
      sentence = ''.join(ch for ch in sentence.lower() if ch not in exclude)
      ngrams.extend(list(everygrams(sentence.split(), max_len=n, min_len=n)))

  unique_ngrams = sorted(set(ngrams))

  output_file = output_file_name + "_unclean.txt"

  with codecs.open(output_file,'w',encoding='utf8') as f:
      for ngram in unique_ngrams:
          line = ngram + (str(ngrams.count(ngram)),)
          for word in line:
              f.write(''.join(word) + ' ')
          f.write('\n')

  return output_file


def clean(unclean_file, output_file_name):
  with codecs.open(unclean_file,'r',encoding='utf8') as read_file:
      with codecs.open(output_file_name+".txt",'w',encoding='utf8') as write_file:
          for line in read_file.readlines():
              if re.match(r'[a-zåäö]+ [a-zåäö]+ [0-9]+', line):
                  write_file.write(line)


n = int(sys.argv[1])
input_file = sys.argv[2]
output_file_name = str(n) + "-grams";

unclean_file = build(n, input_file, output_file_name)
clean(unclean_file)