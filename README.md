# Visualizando a Poesia de Belchior

Projeto final da disciplina Visualização Científica, ministrada pela professora Emanuele Santos. 

**Lucas Cabral** <br>
Universidade Federal do Ceará, Mestrado e Doutorado em Ciências da Computação<br>
2019.2

![Belchior](https://www.urbanarts.com.br/imagens/produtos/123739/0/Ampliada/amar-e-mudar-as-coisas.jpg)
*Arte: [Daniel Brandão](https://www.estudiodanielbrandao.com/)*

Antonio Carlos Belchior, mais conhecido como Belchior (Sobral, 26 de outubro de 1946 – Santa Cruz do Sul, 30 de abril de 2017), foi um compositor cearense entre os mais notórios do cancioneiro popular brasileiro.  Dono de uma obra de grande densidade e complexidade estética, literária e filosófica, suas ricas composições são objeto de estudo acadêmico e um marco da cultura cearense. Este trabalho propõe uma análise de suas composições através de técnicas de processamento de linguagem natural e de visualização de dados. Dado a riqueza poético e musica das composições de Belchior, este trabalho não tem a pretenção de realizar uma análise literária ou linguística aprofundada, mas sim, movido por curiosidade e admiração, utilizar ferramentas computacionacias para explorar os padrões sintáticos e estatísticos que permeiam o conjunto de sua obra. Nos interessa saber:

- Qual a distribuição do tamanho das letras das músicas?
- Quais os termos mais relevantes na obra toda? E por música?
- Quais letras possuem maior similaridade? 
- Qual a polaridade de sentimento e o nível de subjetividade dominante na obra? E por música? 
- Quais são as palavras que mais ocorrem juntas? 

Vamos ver o que conseguimos descobrir!

O código de geração das visualizações, bem como uma breve explicação das análises realizadas, estão neste [notebook](https://github.com/cabrau/visualizando_belchior/blob/master/visualizando_belchior.ipynb).

# Sobre os dados
As letras foram extraídas do site [Letras](https://www.letras.mus.br/) através de um [web-crawler](https://github.com/cabrau/visualizando_belchior/blob/master/scrapping_lyrics.ipynb). Dando como input o nome do artista, o web-crawler percorre a lista de todas as músicas do artista, armazenando em uma tabela o título da música, se é uma das mais tocadas e a letra, descartando músicas cuja composição não seja do artista escolhido.

Após essa coleta, os dados passaram por uma etapa de [extração de features](https://github.com/cabrau/visualizando_belchior/blob/master/pre_processing_text.ipynb) utilizando técnicas de processamento de linguagem natural, incluindo:

* Contagem de palavras por documento
* Tokenização
* Remoção de stopwords
* Normalização
* Extração de palavras-chave
* Distribuição de frequências de tokens
* Extração de nGramas
* Cálculo de matriz termo-documento (TF-IDF)
* Matriz de similaridade de documentos
* Redução de dimensionalidade com UMAP
* Análise de sentimentos
* Modelagem de tópicos

[Quantidade de palavras por música](https://raw.githubusercontent.com/cabrau/visualizando_belchior/master/1_tamanho_musicas.html)

[Termos mais frequentes](https://raw.githubusercontent.com/cabrau/visualizando_belchior/master/2_frequencia%20termos.html)

## Nuvem de palavras
![WordCloud](https://github.com/cabrau/visualizando_belchior/blob/master/wordcloud.png?raw=true)
