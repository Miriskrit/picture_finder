import requests
import urllib.request
import urllib
from bs4 import BeautifulSoup


class Finder:

    def __init__(self, name):
        self.name = name

    def trade(self):
        Links = []
        web_name = urllib.parse.quote_plus(':' + self.name)
        url = 'https://yandex.ru/images/search?text=' + web_name
        source_cod = requests.get(url)
        plain_txt = source_cod.text
        soup = BeautifulSoup(plain_txt, "html.parser")
        for link in soup.findAll('a', {'class': 'serp-item__link'}):
            href = link.get('href')
            new_url = 'https://yandex.ru' + href
            jpg_url = new_url.split('=')[2][:-5:]
            s = jpg_url.replace('%3A%2F%2F', '://').replace('%2F', '/')
            if s[-4:] == '.jpg' or s[-4:] == '.png':
                Links.append(s)
        return Links
