# Classificacao Automatica de Atividades Culturais e Educacionais
# Coleta das atividades do SESC pelo endpoint JSON do site
#
# Integrantes: Beatriz Aparecida de Mello Barbosa (10354067), Bruna Goncalves Corte David (10425696),
#              Henrique Brainer Costa (10420717), Joao Pedro Queiroz de Andrade (10425822),
#              Julia Andrade (10428513)
#
# Conteudo: le os endpoints de cada unidade do SESC, pega os dados de cada atividade e busca a
#           descricao completa na pagina da atividade. Gera um .txt e um .csv.
#
# Alteracoes:
#   2026-09-22 - Julia - primeira versao da coleta pelo endpoint JSON
#   2026-09-23 - Julia - inclusao da descricao completa, lida da pagina de cada atividade
#   2026-09-25 - Bruna - leitura das categorias corrigida e inclusao do publico

import requests
import pandas as pd
from bs4 import BeautifulSoup
import time #apenas para medir o tempo de execução

todas_Atvdds = {} 
count_dados_lidos = 0

# ======================================================
# CONFIGURAÇÃO DE TESTE
# Mudar para None (sem aspas) quando quiser extrair todas as atividades
limite_atividades = None 
# ======================================================

tempo_inicio = time.time() #INICIO DA MEDIÇÃO DE TEMPO!!!!!!!
sessao = requests.Session()
# User-Agent simulando o Microsoft Edge
sessao.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0'})

with open('Atvdds_urls.txt', 'r', encoding='utf-8') as urls:
    for linha in urls:
        # Interrompe a leitura de novos URLs se o limite foi atingido
        if limite_atividades and len(todas_Atvdds) >= limite_atividades:
            break
            
        url_limpa = linha.strip()
        if url_limpa:
            pingada = sessao.get(url_limpa)

            # Verificação ---------------------------------------------
            if pingada.status_code == 200:
                raw_data = pingada.json()

                if 'atividade' in raw_data and raw_data['atividade']:
                    for item in raw_data['atividade']:
                        
                        # Interrompe a extração de atividades se o limite foi atingido
                        if limite_atividades and len(todas_Atvdds) >= limite_atividades:
                            break
                        
                        id_ativ = item.get('id')
                        nome_atvdd = item.get('titulo', 'Sem título')
                        link_parcial = item.get('link', '')
                        link_completo = "https://www.sescsp.org.br" + link_parcial

                        # ======================================================
                        # Extração da descrição via Web Scraping no link da atividade
                        # ======================================================
                        descricao_atvdd = "Descrição não encontrada"
                        if link_parcial:
                            try:
                                page_resp = sessao.get(link_completo, timeout=5)
                                if page_resp.status_code == 200:
                                    soup = BeautifulSoup(page_resp.text, 'html.parser')
                                    
                                    # BUSCA ATUALIZADA com a classe exata apontada por você
                                    conteudo = soup.find('div', class_='principal--post--conteudo')
                                    
                                    if conteudo:
                                        paragrafos = conteudo.find_all('p')
                                    else:
                                        paragrafos = soup.find_all('p')
                                        
                                    textos = [p.get_text(strip=True) for p in paragrafos if len(p.get_text(strip=True)) > 20]
                                    if textos:
                                        descricao_atvdd = " ".join(textos[:3]).replace('\n', ' ').replace('\r', ' ')
                            except Exception as e:
                                descricao_atvdd = "Erro ao acessar página"
                        # ======================================================

                        # Data e hora ------
                        raw_date_FS = item.get('dataPrimeiraSessao', 'Data não especificada')
                        raw_date_LS = item.get('dataUltimaSessao', '')
                        raw_date_PS = item.get('dataProxSessao', '')
                        
                        clean_date_FS = raw_date_FS.replace('T', ' ') if raw_date_FS else ' ' 
                        clean_date_LS = raw_date_LS.replace('T', ' ') if raw_date_LS else ' '
                        clean_date_PS = raw_date_PS.replace('T', ' ') if raw_date_PS else ' '
                        #------------------
                        
                        lista_unidades = [i.get('name') for i in item.get('unidade', []) if i.get('name')]
                        unidade_avdd = ", ".join(lista_unidades)

                        # O campo 'categorias' vem vazio em quase toda atividade.
                        # As categorias de verdade ficam em 'tipos_linguagens', e as mais
                        # especificas ficam dentro de 'children'.
                        lista_categorias = []
                        for j in item.get('tipos_linguagens', []):
                            if j.get('titulo'):
                                lista_categorias.append(j.get('titulo'))
                            for filho in j.get('children', []):
                                if filho.get('titulo'):
                                    lista_categorias.append(filho.get('titulo'))
                        # separador | porque tem nome de categoria com virgula dentro,
                        # como "Shows, Espetaculos e Performances"
                        categoria_atvdd = "|".join(lista_categorias)

                        lista_publico = [p.get('titulo') for p in item.get('publico_tag', []) if p.get('titulo')]
                        publico_atvdd = "|".join(lista_publico)

                        campo_gratuito = item.get('gratuito', '').strip()
                        if campo_gratuito == "":
                            pagamento = "Pago" 
                        else:
                            pagamento = "Gratuito"

                        todas_Atvdds[id_ativ] = {
                            "Nome da Atividade": nome_atvdd,
                            "Descrição": descricao_atvdd,
                            "Data Proxima seção": clean_date_PS,
                            "Data Primeira seção": clean_date_FS,
                            "Data Ultima seção": clean_date_LS,
                            "Unidade": unidade_avdd,
                            "Categorias": categoria_atvdd,
                            "Publico": publico_atvdd,
                            "Acesso": pagamento, 
                            "Link": link_completo
                        }

                count_dados_lidos += 1
            else:
                print(f"Erro. Código de erro: ", pingada.status_code)

print(f"Dados extraídos com sucesso! Total de URLs processados: {count_dados_lidos}. Atividades salvas: {len(todas_Atvdds)}") 
        
#----------------------------------------------------
# Output File (TXT)
with open('Atividades_SESC.txt', 'w', encoding='utf-8') as Atvdds:
    for atividade in todas_Atvdds.values():
        Atvdds.write(f"Nome da Atividade: {atividade['Nome da Atividade']}\n")
        Atvdds.write(f"Descrição: {atividade['Descrição']}\n")
        Atvdds.write(f"Data Próxima sessão: {atividade['Data Proxima seção']}\n")
        Atvdds.write(f"Data Primeira sessão: {atividade['Data Primeira seção']}\n")
        Atvdds.write(f"Data Última sessão: {atividade['Data Ultima seção']}\n")
        Atvdds.write(f"Unidade: {atividade['Unidade']}\n")
        Atvdds.write(f"Categorias: {atividade['Categorias']}\n")
        Atvdds.write(f"Acesso: {atividade['Acesso']}\n")
        Atvdds.write(f"Link: {atividade['Link']}\n")
        Atvdds.write("-" * 50 + "\n\n")

# Output File (CSV)
lista_de_atividades = list(todas_Atvdds.values())
df_atividades = pd.DataFrame(lista_de_atividades)
df_atividades.to_csv("Atividades_SESC.csv", index=False, sep=";", encoding="utf-8-sig")

#---------------------Resultados de tempo!------------
tempo_fim = time.time()
tempo_total = tempo_fim - tempo_inicio
print(f"Tempo total de execução: {tempo_total:.2f} segundos") #excecução mais recente: 22/09/21026 às 21:40, 564 itens extraídos em 696.06 segundos