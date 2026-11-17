# Classificação Automática de Atividades Culturais e Educacionais

Projeto da disciplina de Inteligência Artificial, 7º semestre de Ciência da Computação,
Universidade Presbiteriana Mackenzie, 2026/2. Prof. Dr. Ivan Carlos Alcântara de Oliveira.

| Integrante | RA | E-mail |
|---|---|---|
| Beatriz Aparecida de Mello Barbosa | 10354067 | beatrizaparecida.barbosa@mackenzista.com.br |
| Bruna Gonçalves Corte David | 10425696 | bruna.david@mackenzista.com.br |
| Henrique Brainer Costa | 10420717 | henriquebrainer.costa@mackenzista.com.br |
| João Pedro Queiroz de Andrade | 10425822 | joaopedroqueiroz.andrade@mackenzista.com.br |
| Júlia Andrade | 10428513 | 10428513.andrade@mackenzista.com.br |

## O problema

O SESC e as Fábricas de Cultura publicam muita atividade, e as categorias que elas usam para
organizar tudo isso são pouco precisas. Tem categoria genérica demais, como "Tecnologias e Artes",
que junta um curso de programação e um de pintura sob a mesma etiqueta. Tem categoria que fala do
formato e não do assunto, como "Encontros e Palestras", que apareceu em 98 atividades e em 87 delas
precisou de outra categoria junto para significar alguma coisa. E tem categoria que diz quem
organizou, como "Biblioteca". Como as atividades expiram rápido, reclassificar tudo na mão não é
viável para as instituições.

## O que o projeto faz

É uma API local que recebe a descrição de uma atividade e devolve as categorias mais específicas, em
ordem, avisando quando a resposta deve ser conferida por uma pessoa. As categorias não podiam ser
copiadas dos sites, já que são o problema, por isso descobrimos as categorias nos próprios textos:
transformamos cada descrição em números com um modelo de linguagem em português, agrupamos as
atividades parecidas e demos nome a cada grupo. Saíram 13 categorias, e duas delas, **Reciclagem e
Sustentabilidade** e **Plantas e Alimentação**, não existem como categoria em nenhuma das duas
instituições.

Depois, cada atividade de treino recebeu uma lista de categorias, que pode ter mais de uma, e
treinamos seis classificadores com essas listas. Para medir o resultado, nós cinco rotulamos à mão
100 atividades que ficaram fora do treino. O classificador que vai para a API é o de embeddings com
regressão logística, e os detalhes estão no artigo.

## Como ler este repositório

| Pasta | O que tem |
|---|---|
| `data/` | os dados, da coleta às tabelas geradas e à rotulagem humana, descritos em [`data/README.md`](data/README.md) |
| `notebooks/` | o projeto inteiro, do 01 ao 10, para rodar na ordem |
| `models/` | o classificador e os limites de revisão que a API usa, gerados pelos notebooks 07, 09 e 10 |
| `api/` | a API local |
| `docs/` | as entregas de cada parte (proposta, artigo parcial, artigo final e rubricas) e as figuras do artigo |

| Notebook | O que faz |
|---|---|
| `01_exploratory_analysis.ipynb` | junta as coletas e mede por que as categorias dos sites não servem |
| `02_tfidf_preparation.ipynb` | monta o texto, transforma em números contando palavras e separa treino e teste |
| `03_embeddings_preparation.ipynb` | transforma o mesmo texto em números com o modelo de português |
| `04_tfidf_clustering.ipynb` | agrupa as atividades usando a contagem de palavras |
| `05_embeddings_clustering.ipynb` | agrupa usando os embeddings e nomeia as categorias novas |
| `06_multilabel_exploration.ipynb` | os experimentos que decidiram como dar mais de uma categoria a cada atividade |
| `07_train_only_labels.ipynb` | refaz os grupos só com o treino e dá a cada atividade a sua lista de categorias |
| `08_human_review.ipynb` | a rotulagem feita por nós em 100 atividades do teste, que vira o gabarito |
| `09_classifiers.ipynb` | treina e compara os seis classificadores e salva o melhor para a API |
| `10_review_flags.ipynb` | define quando a API pede revisão humana e mede o acerto em cada categoria |

## Como rodar

```
py -3.11 -m pip install -r requirements.txt
py -3.11 -c "import nltk; nltk.download('stopwords')"
cd notebooks
jupyter notebook
```

Os notebooks rodam na ordem. O 03 baixa o modelo `PORTULAN/serafim-335m-portuguese-pt-sentence-encoder`
na primeira execução e leva cerca de 5 minutos para gerar os vetores das 693 atividades num
computador sem placa de vídeo, e precisa rodar antes do 05 em diante, porque esses vetores não vão
para o GitHub. Os notebooks usam semente fixa, então rodam sempre com o mesmo resultado.

Para subir a API, a partir da pasta do projeto:

```
py -3.11 -m uvicorn api.main:app
```

Depois é só abrir http://127.0.0.1:8000/docs no navegador, mandar o título e a descrição de uma
atividade e ver as categorias voltando, com a probabilidade de cada uma e o aviso de revisão quando
for o caso.

## Artigo e vídeo

O artigo final está em [`docs/part3_submission/`](docs/part3_submission/), junto com a rubrica
preenchida. O vídeo de apresentação está em https://youtu.be/BHkIDcA5YPo.

## Sobre o histórico dos arquivos

Os notebooks 01 a 05 foram reescritos do zero em 25/09, reunindo os testes que fizemos antes para
estudar as bibliotecas e entender os dados, por isso o histórico no cabeçalho deles começa nessa
data. A coleta dos dados é anterior, e essa data aparece nos scripts em `data/01_scraping/` e no
nome dos arquivos em `data/02_raw/`.

## Etapa atual

Parte 3, entrega final: o projeto completo, com o classificador, a API e o artigo final.
