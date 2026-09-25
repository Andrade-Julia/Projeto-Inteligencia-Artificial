# Classificação Automática de Atividades Culturais e Educacionais

Projeto da disciplina de Inteligência Artificial, 7º semestre de Ciência da Computação,
Universidade Presbiteriana Mackenzie, 2026/2. Prof. Dr. Ivan Carlos Alcântara de Oliveira.

| Integrante | RA | E-mail |
|---|---|---|
| Beatriz Aparecida de Mello Barbosa | 10354067 | beatrizaparecida.barbosa@mackenzista.com.br |
| Bruna Gonçalves Corte David | 10425696 | bruna.david@mackenzista.com.br |
| Henrique Brainer Costa | 10420717 | henriquebrainer.costa@mackenzista.com.br |
| João Pedro Queiroz de Andrade | 10425822 | joaopedroqueiroz.andrade@mackenzista.com.br |
| Júlia Andrade | 10428513 | juliaandrade.andrade@mackenzista.com.br |

## O problema

O SESC e as Fábricas de Cultura publicam muita atividade, e as categorias que elas usam para
organizar tudo isso são pouco precisas. Tem categoria genérica demais, como "Tecnologias e Artes",
que junta um curso de programação e um de pintura sob a mesma etiqueta. Tem categoria que fala do
formato e não do assunto, como "Encontros e Palestras", que apareceu em 98 atividades e em 87 delas
precisou de outra categoria junto para significar alguma coisa. E tem categoria que diz quem
organizou, como "Biblioteca". Como as atividades expiram rápido, reclassificar tudo na mão não é
viável para as instituições.

## O que o projeto faz

A ideia é uma API que recebe a descrição de uma atividade e devolve a categoria, ou as categorias,
mais específicas. Para isso precisávamos primeiro de categorias melhores que as atuais, e elas não
podiam ser copiadas dos sites, já que são o problema. Então descobrimos as categorias a partir dos
próprios textos: transformamos cada descrição em números com um modelo de linguagem em português,
agrupamos as atividades parecidas e demos nome a cada grupo.

Duas das categorias que apareceram não existem em nenhuma das duas instituições: **Reciclagem e
Sustentabilidade** e **Plantas e Alimentação**.

## Notebooks

Rodar na ordem, a partir da pasta `notebooks/`.

| Notebook | O que faz |
|---|---|
| `01_exploratory_analysis.ipynb` | junta as coletas e mede por que as categorias dos sites não servem |
| `02_tfidf_preparation.ipynb` | monta o texto e transforma em números contando palavras |
| `03_embeddings_preparation.ipynb` | transforma o mesmo texto em números com o modelo de português |
| `04_tfidf_clustering.ipynb` | agrupa as atividades usando a contagem de palavras |
| `05_embeddings_clustering.ipynb` | agrupa usando os embeddings e nomeia as categorias novas |

A descrição do dataset está em [`data/README.md`](data/README.md).

## Como rodar

```
pip install -r requirements.txt
cd notebooks
jupyter notebook
```

O notebook 03 baixa o modelo `PORTULAN/serafim-335m-portuguese-pt-sentence-encoder` na primeira
execução, e leva cerca de 5 minutos para transformar as 693 atividades em vetores num computador
sem placa de vídeo. Os notebooks usam semente fixa, então rodam sempre com o mesmo resultado.

## Sobre o histórico dos arquivos

Os notebooks deste repositório foram escritos todos no dia 25/09, e o histórico de alterações no
cabeçalho de cada um mostra só essa data.

Antes deles existiram outros notebooks, que usamos para estudar as bibliotecas, testar ideias e
entender os dados, e boa parte do que tentamos ali não deu certo. Quando entendemos melhor o que o
projeto precisava, achamos que reaproveitar aquele material atrapalharia mais do que ajudaria, então
reescrevemos tudo do zero, mais enxuto e na ordem certa, e apagamos os antigos. Como o histórico do
cabeçalho é por arquivo, e os arquivos antigos não existem mais, o que ficou registrado foi a data
da reescrita.

A coleta dos dados é anterior, e essa data aparece nos scripts em `data/scraping/` e no nome dos
arquivos em `data/raw/`.

## Etapa atual

Parte 2 do projeto: dataset, análise exploratória, preparação dos dados e artigo parcial. O
classificador multirrótulo e a API são da Parte 3.
