from pprint import pprint
import requests
from lxml import html
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
import hashlib
client = MongoClient('127.0.0.1', 27017)

db = client['news']
lenta_ru = db.lenta_ru

url = 'https://lenta.ru/'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'}

response = requests.get(url, headers=headers)
dom = html.fromstring(response.text)

news_blocks = dom.xpath("//a[contains(@class, '_topnews')]")

for news in news_blocks:
    doc = {}
    name_news = news.xpath(".//h3[contains(@class, 'card-big__title')]/text() | .//span[contains(@class, 'card-mini__title')]/text()")[0]
    link_news = news.xpath("./@href")
    link_source = url + str(link_news[0])
    time = news.xpath(".//time[contains(@class, 'card-big__date')]/text() | .//time[contains(@class, 'card-mini__date')]/text()")[0]

    hash_link = hashlib.sha224(link_source.encode())
    link_hex = hash_link.hexdigest()
    doc['_id'] = link_hex
    doc['Name'] = name_news
    doc['Source'] = link_source
    doc['Data'] = time
    doc['Link'] = 'lenta.ru'

try:
    lenta_ru.insert_one(doc)
except DuplicateKeyError:
    print(f"Document with id = {link_hex} already exists")

for doc in lenta_ru.find({}):
    pprint(doc)