import requests
import HTMLParser

word = "jag"
url = 'http://tyda.se/search/' + word
payload = {'lang[0]' : 'sv',
          'lang[1]' : 'en'}
page = requests.post(url, data=payload)
if page.status_code != requests.codes.ok:
  print(page.text)
  page.raise_for_status()

output_file = word + "_tyda_translation.html"
chunk_size = 10
with open(output_file, 'wb') as fd:
    for chunk in page.iter_content(chunk_size):
        fd.write(chunk)
