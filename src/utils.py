"""
Funções utilizadas na obtenção, processamento e análise de letras
"""

import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import requests
import re
import os, sys
from unicodedata import normalize

def remove_accent(txt):
    return normalize('NFKD', txt).encode('ASCII', 'ignore').decode('ASCII')

def clean_html(raw_html):
    """
    Remove html tags from a given string
    """
    CLEANR = re.compile('<.*?>') 
    clean_text = re.sub(CLEANR, ' ', raw_html)
    clean_text = re.sub(' +', ' ', clean_text)
    return clean_text

def parse_lyric(url, links_most_played = None):
    """
    Recebe o link de uma letra e, opcionalmente, uma lista com os links das músicas mais tocadas.
    Retorna titulo, compositor, primeiro compositor, se é mais tocada e o texto da letra
    """
    # testa se é uma das músicas mais tocadas
    most_played = False
    if links_most_played and url in links_most_played:
        most_played = True        
    # acessa o link da letra
    try:
        req = requests.get(url)
    except requests.exceptions.RequestException as e: 
        print(e)        
    content = req.content
    soup = BeautifulSoup(content, 'html.parser')
    
    #compositor
    #<div class="letra-info_comp">
    html_comp = soup.find_all("div", {"class": "letra-info_comp"})
    html_comp = str(html_comp)
    try:
        composer = html_comp.split('Composição: ')[1]
        composer = composer.split('<a')[0]
        composer = composer[0:-2].strip()
    except:
        composer = 'Não identificado'
    first_composer = composer.split(' / ')[0] 
    
    
    #título da música
    #<div class="cnt-head_title">
    html_title = soup.find_all("div", {"class": "cnt-head_title"})
    html_title = str(html_title)
    title = html_title.split('<h1>')[1]
    title = title.split('</h1>')[0]
    
    #letra da música
    html = soup.find_all("div", {"class": "cnt-letra p402_premium"})
    html = str(html)
    verses = html.split('<p>')
    verses = verses[1:]

    lyric = ''
    for verse in verses:
        # remove tags html        
        verse = clean_html(verse)
        lyric += verse

    lyric = lyric.strip()
    return title, composer, first_composer, most_played, lyric

