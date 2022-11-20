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
import string
import nltk
from sklearn.feature_extraction.text import CountVectorizer
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter

# insert dir of python scripts in the path
module_path = os.path.abspath(os.path.join(os.pardir))
if module_path not in sys.path:
    sys.path.append(module_path)

# stopwords inglês
stopwords = nltk.corpus.stopwords.words('english')
# stopwords pt-br
stopwords_path = os.path.join(module_path, 'linguistic_resources', 'stopwords.txt')
with open(stopwords_path) as f:
       for line in f:
            line = line.replace(' ','')
            line = line.replace('\n','')
            stopwords.append(line)

def preprocess(text):
    """
    Retorna um dado texto normalizado: caixa baixa, removendo pontuação, removendo stopwords
    """
    # caixa baixa
    text = text.lower()
    # remover pontuação
    punctuation = string.punctuation
    for punct in punctuation:
        text = text.replace(punct, ' ')
    # remove espaços em excesso
    text = re.sub(' +', ' ', text)

    # remove stopwords
    tokens = [t for t in text.split() if t not in stopwords and len(t) > 2]
    text = ' '.join(tokens)

    return text

def get_keywords(text, n):
    tokens = text.split()
    counter_tokens = Counter(tokens).most_common(n)
    keywords = [token[0] for token in counter_tokens]
    keywords = ', '.join(keywords)
    return keywords  

def get_top_n_ngrams(corpus, ngram = (1,1), n=None):
    """
    Para uma dada lista de strings, calcula os n-gramas mais frequentes
    """
    if type(corpus) == str:
        corpus = [corpus]
    vec = CountVectorizer(ngram_range = ngram).fit(corpus)
    bag_of_words = vec.transform(corpus)
    sum_words = bag_of_words.sum(axis=0) 
    words_freq = [(word, sum_words[0, idx]) for word, idx in vec.vocabulary_.items()]
    words_freq = sorted(words_freq, key = lambda x: x[1], reverse=True)
    return words_freq[:n]

def build_ngram_df(corpus, ngram = (1,1), n=None,):
    """
    Cria um dataframe de n-gramas
    """
    ngrams = get_top_n_ngrams(corpus, ngram, n)
    df1 = pd.DataFrame(ngrams, columns = ['ngrams' , 'count'])
    df1 = df1.groupby('ngrams').sum()['count'].sort_values(ascending=False)
    return df1

def plot_ngrams(ngrams, col = 'C0', orientation = 'vertical'):
    """
    Gráfico de barras dos n-gramas mais frequentes
    """
    labels = list(ngrams.index)
    values = list(ngrams.values)
    #
    if orientation == 'vertical':
        g = sns.barplot(y=labels, x=values, color = col)
        for p in g.patches:
            g.annotate(format(p.get_width(), '.0f'), (p.get_width(), 
                                                       p.get_y() + p.get_height()/2.), ha = 'center', 
                       va = 'center', xytext = (10, 0), textcoords = 'offset points')
    else:
        plt.xticks(values, labels, rotation='vertical')
        g = sns.barplot(x=labels, y=values, color = col) 
        for p in g.patches:
            g.annotate(format(p.get_height(), '.0f'), (p.get_x() + p.get_width() / 2., 
                                                       p.get_height()), ha = 'center', 
                       va = 'center', xytext = (0, 5), textcoords = 'offset points') 

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

