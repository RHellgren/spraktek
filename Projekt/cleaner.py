import re
import codecs

with codecs.open('bigrams.txt','r',encoding='utf8') as read_file:
    with codecs.open('bigrams_clean.txt','w',encoding='utf8') as write_file:
        for line in read_file.readlines():
            if re.match(r'[a-zåäö]+ [a-zåäö]+ [0-9]+', line):
                write_file.write(line)
