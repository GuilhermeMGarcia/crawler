import requests
from bs4 import BeautifulSoup


URL_AUTOMOVEIS = 'https://django-anuncios.solyd.com.br'


def buscar(url):
    try:
        resposta = requests.get(url)
        if resposta.status_code == 200:
            return resposta.text
        else:
            print('erro ao fazer requisiçao')
    except Exception as error:
        print('erro ao fazer requisiçao')
        print(error)


def parsing(resposta_html):
    try:
        soup = BeautifulSoup(resposta_html, 'html.parser')
        return soup
    except Exception as error:
        print('erro ao fazer parsing')
        print(error)


def encontar_link(soup):
    cards_pai = soup.find("div", class_="ui three doubling link cards")
    cards = cards_pai.find_all('a', class_="card")
    links = []
    for card in cards:
        link = card['href']
        links.append(link)
    return links


resposta = buscar(URL_AUTOMOVEIS)
if resposta:
    soup = parsing(resposta)
    if soup:
        links = encontar_link(soup)
        for link in links:
            print(link)

