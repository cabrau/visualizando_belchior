# Visualizando a Poesia de Belchior
*Por Lucas Cabral*

![Belchior](capa.png)<br>

Antonio Carlos Belchior, mais conhecido somente como Belchior (Sobral, 26 de outubro de 1946 – Santa Cruz do Sul, 30 de abril de 2017), foi um compositor cearense entre os mais notórios do cancioneiro popular brasileiro.  Dono de uma obra de grande densidade e complexidade estética, literária e filosófica, suas ricas composições são objeto de estudo acadêmico e um marco da cultura cearense. 

Este trabalho propõe uma análise de suas composições através de técnicas de processamento de linguagem natural (NLP) e de visualização de dados. Dado a riqueza poético e musical das composições de Belchior, este trabalho não tem a pretensão de realizar uma análise literária ou linguística aprofundada de cada letra. Mas sim, movido por curiosidade e admiração, utilizar ferramentas computacionais para explorar os padrões sintáticos e estatísticos que permeiam o conjunto de sua obra, criando uma nova perspectiva sobre o macro. Nos interessa saber:

- Qual a distribuição do tamanho das letras das músicas? E a variabilidade léxica dessas composições?
- Quais os termos mais relevantes na obra toda? E por música? Quais os termos mais raros?
- Quais letras possuem maior similaridade entre si? 
- Qual a polaridade de sentimento e o nível de subjetividade dominante na obra? E por música? 
- Quais são os termos que mais ocorrem em conjunto? 

Vamos ver o que conseguimos descobrir!

O código de geração das visualizações encontra-se neste [notebook](https://github.com/cabrau/visualizando_belchior/blob/master/notebooks/lyrics_analysis.ipynb).

# Sobre os dados
As letras foram extraídas do site [Letras](https://www.letras.mus.br/) através de um [web-crawler](https://github.com/cabrau/visualizando_belchior/blob/master/notebooks/web_scrapping.ipynb). Fornecendo como entrada o nome do artista, o web-crawler percorre a lista de todas as músicas do artista, armazenando em uma tabela o título da música, se é uma das mais tocadas e a letra, descartando músicas cuja composição não seja do artista escolhido. Essa metodologia pode ser repetida para outros artistas de interesse. 

Ao total, foram extraídos **93** composições. Após essa coleta, os dados passaram por uma etapa de pré-processamento e extração de atributos utilizando técnicas de [NLP](https://en.wikipedia.org/wiki/Natural_language_processing), incluindo:

* Contagem de palavras por documento
* Tokenização
* Remoção de stopwords
* Normalização
* Extração de palavras-chave
* Distribuição de frequências de tokens
* Extração de n-gramas
* Cálculo de variabilidade léxica
* Cálculo de matriz termo-documento (TF-IDF)
* Matriz de similaridade de documentos
* Análise de sentimentos

# Quantidade de palavras nas letras

Nestes gráficos podemos explorar a distribuição de quantidade de palavras de todas as composições e as palavras-chave de cada comṕosição. Pode-se realizar seleções nos histogramas para observar somente as músicas desejadas. 

Essa página também contém um gráfico de dispersão mostrando a relação entre a quantidade de palavras nas músicas e a sua variabilidade léxica. Ou seja, a proporção de palavras únicas no total de palavras utilizadas em cada letra.<br>
### [Gráfico de barras, histograma e gráfico de dispersão](visualizations/belchior/palavras_por_musicas.html)


# Termos mais frequentes
Quais os termos que mais se repentem na obra e em quais músicas eles aparecem e quais termos aparecem somente uma única vez na obra completa.<br>
### [Gráfico de barras](visualizations/belchior/frequencia_dos_termos.html)<br>
![Nuvem de palavras](https://github.com/cabrau/visualizando_belchior/blob/master/wordcloud.png?raw=true)

# Co-Ocorrência de Termos

Além de conhecer os termos mais utilizados, podemos visualizar como eles co-ocorrem através de uma rede. Cada nó do grafo é uma palavra e uma aresta significa que estas ocorrem juntas.<br>
### [Gráfico de rede](visualizations/belchior/rede_co_ocorrencia.html)


# Similaridade entre Composições
Uma técnica bastante utilizada em processamento de linguagem natural é o cáculo do [TF-IDF](https://pt.wikipedia.org/wiki/Tf%E2%80%93idf). O valor TF-IDF (abreviação do inglês *term frequency–inverse document frequency*), é uma medida estatística que tem o intuito de indicar a importância de uma palavra de um documento em relação a uma coleção de documentos ou em um corpus linguístico. 

Através desse cálculo pode-se vetorizar um documento em um espaço n-dimensional, onde n é o tamanho do vocabulário. Assim cada indice dos vetores represanta um signo linguístico do vocabulário, e o seu valor é o tf-idf daquele termo naquele documento. Vetorizando os documentos, pode-se comparar quais são mais similares. Uma métrica básica é a [distância cosseno](https://en.wikipedia.org/wiki/Cosine_similarity). 

Neste gráfico, podemos ter uma visão geral da obra, considerando as composições mais similares pelas métricas já citadas.<br>

### [Matriz de Similaridade](visualizations/belchior/similaridade_musicas.html)


# Análise de Sentimentos
Esta análise foi realizada utilizando a biblioteca [TextBlob](https://textblob.readthedocs.io/en/dev/). 
Esta biblioteca atribui a cada palavra presente em seu léxico um valor de polaridade (de -1 a 1) e subjetividade (0 a 1), além de um valor de modificador que pode intensificar ou reduzir o valor da próxima palavra, como no caso de adjetivos por exemplo. Na documentação encontramos o seguinte comentário:

```python
# Each word in the lexicon has scores for:
# 1)     polarity: negative vs. positive    (-1.0 => +1.0)
# 2) subjectivity: objective vs. subjective (+0.0 => +1.0)
# 3)    intensity: modifies next word?      (x0.5 => x2.0)
```

A biblioteca análisa sintaticamente a sentença, identificando a classe gramatical de cada palavra e atribuindo valores diferentes para palavras polissêmicas. Entretanto, o léxico que a biblioteca utiliza é em inglês. Portanto, foi necessário traduzir cada letra para este idioma, utilizando a mesma biblioteca, para então ser realizada a análise de sentimento. 

É necessário considerar as limitações dessa abordagem. Primeiro, em algumas composições Belchior explora o uso de linguagem abstrata, utilizando palavras que não são reconhecidos pelo vocabulário. Além disso, não é muito claro na documentação do TextBlob o significado das escalas de subjetividade e polaridade ou como estes níveis foram atribuídos a cada palavra no léxico. Uma outra limitação importante é que essa abordagem de pontuar cada palavra sem uma análise contextual falha em reconhecer ironias. Por último, não sabe-se com exatidão o efeito da tradução na análise de sentimento. Nas palavras de Robert Frost, "poesia é o que se perde na tradução". Apesar de tudo, essa técnica permitiu uma exploração interessante do conjunto da obra do compositor e pode ser um passo inicial para análises mais aprofundadas. As categorias discretas de polaridade foram definidas da seguinte maneira:

* x < -0.1 = Negativo
* -0.1 <= x <= 0.1 = Neutro
* x > 0.1 = Positivo

### [Análise de sentimentos](visualizations/belchior/analise_sentimentos.html)
