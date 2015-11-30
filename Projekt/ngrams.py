import codecs
from nltk import everygrams
import string

sentences = []
with codecs.open('korpus.txt','r',encoding='utf8') as f:
   for line in f:
       sentences.append(line)

bigrams = []
exclude = set(string.punctuation)
for sentence in sentences:
    sentence = ''.join(ch for ch in sentence.lower() if ch not in exclude)
    bigrams.extend(list(everygrams(sentence.split(), max_len=2, min_len=2)))

unique_bigrams = sorted(set(bigrams))

with codecs.open('bigrams.txt','w',encoding='utf8') as f:
    for bigram in unique_bigrams:
        line = bigram + (str(bigrams.count(bigram)),)
        for word in line:
            f.write(''.join(word) + ' ')
        f.write('\n')