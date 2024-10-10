import requests
from bs4 import BeautifulSoup
import string
import os

def soup(u):
    r = requests.get(u)
    return BeautifulSoup(r.content, 'html.parser')

def search_article(u,ub,t):
    articles = soup(u).find_all('article')

    for title in articles:
        if title.find('span', {'data-test':'article.type'}).text == t:
            article_name = title.find('a', {'data-track-action':'view article'}).text
            file_name =''.join([l if l not in string.punctuation else '' for l in article_name]).strip().replace(' ', '_')
            article = soup(ub + title.find('a', {'data-track-action': 'view article'})['href']).find('p', {"class": "article__teaser"})
            file = open(file_name + '.txt', 'wb')
            file.write(article.text.encode(encoding='utf-8'))
            file.close()

url = 'https://www.nature.com/nature/articles?sort=PubDate&year=2020&page='
url_base = 'https://www.nature.com/nature'
page = int(input())
article_type = input()

for p in range(1,page+1,1):
    if 'Page_'+str(p) not in os.listdir():
        os.mkdir('./Page_' + str(p))
    os.chdir('./Page_' + str(p))
    search_article(url + str(p), url_base, article_type)
    os.chdir('../')

print('Data saved!')

