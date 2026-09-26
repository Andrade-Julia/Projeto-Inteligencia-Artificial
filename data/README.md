# Dataset

Atividades culturais e educacionais publicadas pelo SESC São Paulo e pelas Fábricas de Cultura,
coletadas pelo grupo. São 705 atividades, e 693 depois de tirar as repetidas.

Os dados são públicos: as duas instituições divulgam sua programação nos próprios sites, e cada
atividade traz título, descrição, unidade, data e as categorias que a instituição atribuiu. Não há
dado de pessoa nenhuma.

## Coletas

| Arquivo | Conteúdo |
|---|---|
| `raw/fabricas_activities_2026-09-23.csv` | 141 atividades das Fábricas de Cultura, 6 unidades, 19 categorias, uma categoria por atividade |
| `raw/sesc_activities_2026-09-23.csv` | 564 atividades do SESC, 8 unidades, com a descrição completa |
| `raw/sesc_categories_2026-09-25.csv` | 582 atividades do SESC com as categorias e o público, coletadas depois para corrigir o campo errado (ver abaixo) |

Os arquivos de `raw/` não são alterados. Coleta nova entra como arquivo novo, com a data no nome.

Em `raw/original_collection/` fica o `Atividades_SESC.txt`, que é a mesma coleta do SESC no formato
de texto que o script também gera. Guardamos porque foi o arquivo da coleta original.

## Como os dados foram coletados

Os dois scripts estão em `scraping/`.

O SESC carrega a programação do site por um endpoint que devolve JSON, então `Sesc_Atividades.py` pede
esse JSON para cada unidade e depois abre a página de cada atividade para pegar a descrição inteira,
que não vem no JSON. As Fábricas não têm um endpoint assim, então `Fabricas_de_cultura.py` abre o site
num navegador com Selenium, clica em carregar mais até o fim da lista e lê os dados da tela.

**O erro que encontramos na primeira coleta do SESC:** o script lia o campo `categorias` do JSON,
que vem vazio em 91,3% das atividades. As categorias de verdade estão em `tipos_linguagens`, com as
mais específicas dentro de `children`, e o público em `publico_tag`. Como o site parecia estar sem
categoria e não estava, refizemos a leitura e guardamos o resultado em
`sesc_categories_2026-09-25.csv`. O `Sesc_Atividades.py` já está corrigido, então quem rodar hoje
recebe as categorias direto.

As duas coletas do SESC são de dias diferentes, 23 e 25 de setembro, e as atividades expiram rápido:
483 das 564 descrições acharam a categoria correspondente pelo link, e as outras saíram do ar nesse
intervalo.

## Tabelas geradas pelos notebooks

Ficam em `processed/` e são reconstruídas ao rodar os notebooks na ordem.

| Arquivo | Vem de | Conteúdo |
|---|---|---|
| `activities.csv` | notebook 01 | as duas instituições numa tabela só |
| `activities_prepared.csv` | notebook 02 | com o texto montado e a divisão treino/teste |
| `embeddings.npy` | notebook 03 | um vetor de 1024 números por atividade |
| `activities_clustered_tfidf.csv` | notebook 04 | agrupamento feito com TF-IDF |
| `activities_clustered.csv` | notebook 05 | agrupamento por embeddings e a categoria nova de cada atividade |
| `clusters_summary.csv` | notebook 05 | os 16 grupos com palavras, exemplos e o nome que demos |
| `silhouette_tfidf.csv` | notebook 04 | qualidade do agrupamento por número de grupos |

## Colunas da tabela principal

| Coluna | O que é |
|---|---|
| `source` | SESC ou Fábricas de Cultura |
| `unit` | unidade onde a atividade acontece |
| `title` | título da atividade |
| `description` | descrição publicada pela instituição |
| `original_categories` | as categorias que a instituição atribuiu, separadas por `\|` |
| `audience` | público indicado, só o SESC publica |
| `link` | endereço da atividade, só o SESC publica |
| `text` | título e descrição juntos, que é o que vai para o modelo |
| `split` | `train` ou `test` |
| `cluster` | grupo em que a atividade caiu |
| `category` | a categoria nova, criada neste projeto |

## Limitações

São duas instituições, as duas de São Paulo, então a base não representa o país. A quantidade de
atividades por categoria é bem desigual: Esporte tem 135 e Plantas e Alimentação tem 17. Além disso,
parte das descrições mistura o texto da atividade com aviso de inscrição e de vaga, o que atrapalha
quem tenta agrupar as atividades por assunto.
