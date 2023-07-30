from collections import deque
import re

from bs4 import BeautifulSoup
import requests
import urllib.parse

user_url = str(input('[+] masukan url: '))
urls = deque([user_url])
# print(urls)
scraped_urls = set()
emails = set()
count = 0
limit = int(input('[+] Masukan limit pencarian: '))

try:
        while True:
                count += 1
                if count > limit:
                        break
                
                print(urls.popleft())
                url = urls.popleft()
                
                scraped_urls.add(url)
                parts = urllib.parse.urlsplit(url)
                base_url =  f'{parts.scheme}://{parts.netloc}'
                path = url[:url.rfind('/')+1] if '/' in parts.path else url

                print(f'{count} Memproses {url}')

                try:
                        response = requests.get(url)
                except(requests.exceptions.MissingSchema, requests.exceptions.ConnectionError):
                        continue
                
                new_emails = set(re.findall(r'[a-z0-9\.\-+_]+@\w+\.+[a-z\.]+', response.text, re.I))
                emails.update(new_emails)

                soup = BeautifulSoup(response.text, 'html.parser')
                for anchor in soup.find_all('a'):
                        link = anchor.attrs['href'] if 'href' in anchor.attrs else ''
                        if link.startswith('/'):
                                link = base_url + link
                        elif not link.startswith('http'):
                                link = path + link

                        if not link in urls and not link in scraped_urls:
                                urls.append(link)

except KeyboardInterrupt:
        print('[-] Closing!')

print('\n Proses selesai!')
print(f'\n{len(emails)}email ditemukan \n ===============================================')

for mail in emails:
        print('  '+mail)
print('\n')