import re
import threading

import requests
from bs4 import BeautifulSoup


URL_AUTOMOVEIS = 'https://django-anuncios.solyd.com.br'

LINKS = []
TELEFONES = []

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


def descobrir_telefones():
    while True:
        try:
            link_anuncio = LINKS.pop(0)
        except:
            return
        resposta_anuncio = requisicao(URL_AUTOMOVEIS + link_anuncio)

        if resposta_anuncio:
            soup_anuncio = parsing(resposta_anuncio)
            if soup_anuncio:
                telefone = encontrar_numero(soup_anuncio)
                if telefone:
                    print(f'Telefone encontrado {telefone}')
                    TELEFONES.append(f'Link: {link_anuncio} Telefone: {telefone}')
                    salvar_telefone(link_anuncio, telefone)
                else:
                    TELEFONES.append(f'Link: {link_anuncio} Telefone: NONE')


def salvar_telefone(link,telefone):
    try:
        with open('telefone.csv', 'a') as arquivo:
            arquivo.write(f'{link}: {telefone}\n')
    except:
        print('Erro ao salvar telefone')

if __name__ == '__main__':
    resposta_busca =requisicao(URL_AUTOMOVEIS)
    if resposta_busca:
        soup_busca = parsing(resposta_busca)
        if soup_busca:
            LINKS = encontar_link(soup_busca)
            THREAD = []
            for i in range(2):
                t = threading.Thread(target=descobrir_telefones())
                THREAD.append(t)

            for t in THREAD:
                t.start()

            for t in THREAD:
                t.join()

            print('-------------------------------------')
            for telefone in TELEFONES:
                print(telefone)
            print('-------------------------------------')


