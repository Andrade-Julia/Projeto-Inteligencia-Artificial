# Classificação Automática de Atividades Culturais e Educacionais
# API - categorias de uma atividade a partir do título e da descrição
#
# Integrantes: Beatriz Aparecida de Mello Barbosa (10354067), Bruna Gonçalves Corte David (10425696),
#              Henrique Brainer Costa (10420717), João Pedro Queiroz de Andrade (10425822),
#              Júlia Andrade (10428513)
#
# Conteúdo: protótipo local que recebe o título e a descrição de uma atividade e devolve as categorias em
#           ordem, a probabilidade de cada uma e se a resposta precisa de revisão humana. As categorias
#           vêm do classificador de embeddings com regressão logística (notebook 09), e os dois avisos de
#           revisão são os do notebook 10, tudo salvo em models/.
#           Para rodar, a partir da pasta do projeto: py -3.11 -m uvicorn api.main:app
#           Depois, abrir http://127.0.0.1:8000/docs no navegador.
#
# Alterações:
#   27/10/2026 - Bruna - primeira versão
#   16/11/2026 - Bruna - versão final e testes

import os                                                   # monta o caminho da pasta models/
import json                                                 # lê os limites de revisão
import joblib                                               # lê o classificador salvo no notebook 09
import numpy as np                                          # contas com vetores
import pandas as pd                                         # lê o nome de cada grupo
from fastapi import FastAPI, Body                           # cria a API e recebe o texto no corpo do pedido
from sentence_transformers import SentenceTransformer       # transforma o texto em embedding

# ====================================================================================================
#                              CARREGADO UMA VEZ SÓ, QUANDO A API SOBE
# ====================================================================================================
models_folder = os.path.join(os.path.dirname(__file__), "..", "models")                                                  # a pasta models/ fica ao lado da pasta api/

serafim_model = SentenceTransformer("PORTULAN/serafim-335m-portuguese-pt-sentence-encoder")                                # o mesmo modelo de embeddings do notebook 03
api_classifier = joblib.load(os.path.join(models_folder, "classifier.joblib"))                                            # o classificador, o corte de cada categoria e a ordem das categorias (notebook 09)
cluster_centers = np.load(os.path.join(models_folder, "cluster_centers.npy"))                                            # os 16 centros, calculados só com o treino (notebook 07)
cluster_names = pd.read_csv(os.path.join(models_folder, "cluster_names.csv"), sep=";", encoding="utf-8-sig").sort_values("cluster")   # a categoria de cada grupo, na ordem dos centros
review_limits = json.load(open(os.path.join(models_folder, "review_limits.json"), encoding="utf-8"))                     # as beiradas e a menor probabilidade aceita (notebook 10)

category_names = list(api_classifier["category_names"])                                                                   # as 13 categorias, na ordem das colunas do classificador
normalized_centers = cluster_centers / np.linalg.norm(cluster_centers, axis=1, keepdims=True)                            # centros com comprimento 1, para o produto dar o cosseno
clusters_of_each_category = [(cluster_names["category"] == category_name).values for category_name in category_names]   # os grupos de cada categoria (Esporte tem 3, Shows tem 2)

app = FastAPI(title="Classificação de atividades culturais e educacionais", description="Protótipo local: recebe o título e a descrição de uma atividade e devolve as categorias, em ordem, e se a resposta precisa de revisão humana.")   # a página /docs usa esse título


# ====================================================================================================
#                                AS CATEGORIAS: O CLASSIFICADOR
# ====================================================================================================
def categories_of(probabilities):
    categories_from_most_likely = np.argsort(-probabilities)                            # da mais provável para a menos
    categories = []                                                                     # a resposta, em ordem
    for category_position in categories_from_most_likely:
        if probabilities[category_position] >= api_classifier["thresholds"][category_position]:
            categories.append({"category": category_names[category_position], "probability": round(float(probabilities[category_position]), 3)})   # categoria acima do próprio corte
    if not categories:
        best = categories_from_most_likely[0]                                           # nenhuma passou do corte: entra a mais provável, como no notebook 09
        categories.append({"category": category_names[best], "probability": round(float(probabilities[best]), 3)})
    return categories


# ====================================================================================================
#                                OS AVISOS DE REVISÃO (NOTEBOOK 10)
# ====================================================================================================
def review_reasons_of(embedding, probabilities):
    normalized_embedding = embedding / np.linalg.norm(embedding)                                                         # comprimento 1
    similarity_to_clusters = normalized_centers @ normalized_embedding                                                   # cosseno com cada um dos 16 centros
    similarity_to_categories = np.array([similarity_to_clusters[clusters].max() for clusters in clusters_of_each_category])   # vale o grupo mais parecido de cada categoria
    closest_category = category_names[similarity_to_categories.argmax()]                                                 # a categoria do grupo mais parecido

    review_reasons = []                                                                                                   # por que uma pessoa deveria conferir
    if similarity_to_categories.max() < review_limits["borders"][closest_category]:
        review_reasons.append("a atividade não se parece com nenhum grupo conhecido")                                     # sinal 1
    if probabilities.max() < review_limits["minimum_top_probability"]:
        review_reasons.append("o classificador está em dúvida: nenhuma categoria tem probabilidade alta")                  # sinal 2
    return review_reasons


# ====================================================================================================
#                                          A ROTA
# ====================================================================================================
@app.post("/classify")
def classify(description=Body(..., embed=True), title=Body("", embed=True)):
    text = title + ". " + description if title else description                       # o mesmo formato dos notebooks: título, ponto, descrição
    embedding = serafim_model.encode([text])[0]                                        # o texto vira um vetor de 1.024 números
    probabilities = api_classifier["classifier"].predict_proba([embedding])[0]         # uma probabilidade por categoria
    review_reasons = review_reasons_of(embedding, probabilities)                       # os dois sinais do notebook 10
    return {"categories": categories_of(probabilities), "needs_human_review": len(review_reasons) > 0, "review_reasons": review_reasons}
