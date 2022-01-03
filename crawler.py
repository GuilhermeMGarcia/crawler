import re

import requests
from bs4 import BeautifulSoup


URL_AUTOMOVEIS = 'https://django-anuncios.solyd.com.br'


def requisicao(url):
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
    try:
        cards_pai = soup.find("div", class_="ui three doubling link cards")
        cards = cards_pai.find_all('a', class_="card")
    except:
        print('erro ao encontrar link')
        return

    links = []
    for card in cards:
        try:
            link = card['href']
            links.append(link)
        except:
            pass
    return links


def encontrar_numero(soup):
    try:
        descricao = soup.find_all('div', class_="sixteen wide column")[2].p.get_text().strip()
    except:
        print('erro ao encontrar numero')
        return

    regex = re.findall(r"\(?0?([1-9]{2})[ \-\.\)]{0,2}(9[ \-\.]?\d{4})[ \-\.]?(\d{4})", descricao)
    if regex:
        return regex


resposta_busca = requisicao(URL_AUTOMOVEIS)
if resposta_busca:
    soup_busca = parsing(resposta_busca)
    if soup_busca:
        links = encontar_link(soup_busca)
        for link in links:
            reposta_anuncio = requisicao(URL_AUTOMOVEIS + link)
            print(link)
            if reposta_anuncio:
                soup_anuncio = parsing(reposta_anuncio)
                numero = encontrar_numero(soup_anuncio)
                if numero:
                    print(numero)
                else:
                    print('nao foi encontrado numero')