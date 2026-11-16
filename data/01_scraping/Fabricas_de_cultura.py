# Classificacao Automatica de Atividades Culturais e Educacionais
# Coleta das atividades das Fabricas de Cultura pelo navegador
#
# Integrantes: Beatriz Aparecida de Mello Barbosa (10354067), Bruna Goncalves Corte David (10425696),
#              Henrique Brainer Costa (10420717), Joao Pedro Queiroz de Andrade (10425822),
#              Julia Andrade (10428513)
#
# Conteudo: abre a programacao das Fabricas de Cultura no navegador, clica no botao de carregar
#           mais ate o fim da lista e guarda nome, categoria, unidade, data e descricao de cada
#           atividade num .csv.
#
# Alteracoes:
#   2026-09-22 - Julia - primeira versao usando Selenium
#   2026-09-23 - Julia - coleta da descricao completa de cada atividade
#   2026-09-25 - Bruna - correcao do comentario das unidades coletadas

import csv
import time # para evitar que o programa entenda a demora de uma requisição na internet como "acabaram os botões"
from selenium import webdriver # Para trabalhar usando o edge, tb existe o do chrome, firefox... etc
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By

itens_lidos = 0

servico = Service()
try:
    navegador = webdriver.Edge(service=servico) 
except:
    print("Erro no Webdriver - não instalado ou sem permissão ou desatualizado")
    exit()

dados_list = []

try:
    # Unidades coletadas: Jacana, Jardim Sao Luis, Vila Nova Cachoeirinha, Nucleo Taipas,
    # Nucleo Luz, Brasilandia e Capao Redondo
    url = "https://www.fabricasdecultura.org.br//programacao-cultural/?local=jacana%2Bjardim-sao-luis%2Bvila-nova-cachoeirinha%2Bnucleo-taipas%2Bnucleo-luz%2Bbrasilandia%2Bcapao-redondo"
    navegador.get(url)

    time.sleep(3) # O codigo espera 3 segundos antes de começar a trabalhar, ele "espera o site carregar"

    while True:
        atvdds = navegador.find_elements(By.CLASS_NAME, "programacao-card")
        qtd_atvdds_tela = len(atvdds)

        # Se a quantidade na tela for igual ao que já processamos antes do clique, 
        # significa que não foram carregados mais dados
        if qtd_atvdds_tela == itens_lidos:
            print("Fim da pág")
            break 
            
        for atvdd in atvdds[itens_lidos:]:
            try:
                nome = atvdd.find_element(By.CSS_SELECTOR, ".titulo.mb-1").text
            except:
                nome = "Sem título"
            try:
                categoria = atvdd.find_element(By.CSS_SELECTOR, ".programacao-categoria").text
            except:
                categoria = "Sem categoria"
            try:
                unidade = atvdd.find_element(By.CSS_SELECTOR, "div.col > p.d-inline-flex.mt-3").text 
            except:
                unidade = "Sem unidade"
            try:
                data = atvdd.find_element(By.CSS_SELECTOR, "p.d-inline-flex.align-items-center.pe-2.mt-3").text 
            except:
                data = "Sem data"
            try:
                img_elemento = atvdd.find_element(By.CSS_SELECTOR, ".imagem-programacao-card img") # acha a imagem 
                img = img_elemento.get_attribute("src")
            except:
                img = "Sem imagem"

            # ++++++++++++++++++++++Extração da descrição (Interação com o modal)+++++++++++++++++++++++++
            try:
                # 1. Rola a tela até o card atual
                navegador.execute_script("arguments[0].scrollIntoView({block: 'center'});", atvdd)
                time.sleep(0.5) 
                
                # 2. Clica no card para abrir a janela modal(bloquinho)
                atvdd.click()
                time.sleep(1.5) # Aumenta o tempo de pausa para garantir que o modal(bloquinho) carregue por completo
                
                # 3. Busca o modal ativo na tela
                modal_ativo = navegador.find_element(By.CSS_SELECTOR, "div.modal[style*='display: block']")
                
                # 4. Extrai o texto da div class="wysiwyg" mostrada na imagem -->> A div class encontrada me parece estranha, necessidade de revisar em extrações maiores
                # Usamos div.wysiwyg para ser exato ao que está na imagem inspecionada
                elemento_descricao = modal_ativo.find_element(By.CSS_SELECTOR, "div.wysiwyg")
                descricao = elemento_descricao.text
                
                # 5. Clica no "X" para fechar o modal
                btn_fechar = modal_ativo.find_element(By.CSS_SELECTOR, ".btn-close")
                btn_fechar.click()
                time.sleep(0.5) 
                
            except Exception as e:
                descricao = "Sem descrição"
                
                # SISTEMA DE SEGURANÇA (FALLBACK)
                try:
                    webdriver.ActionChains(navegador).send_keys('\x1b').perform() # Envia tecla ESC
                    time.sleep(0.5)
                except:
                    pass

            dados_list.append([nome, categoria, unidade, data, img, descricao])
            
        itens_lidos = qtd_atvdds_tela
        
        # Clicar no botão de carregar mais:
        try:
            botao = navegador.find_element(By.CSS_SELECTOR , "button.btn.btn-programacao.carregar-mais-programacao")
            navegador.execute_script("arguments[0].scrollIntoView({block: 'center'});", botao) 
            time.sleep(1)
            navegador.execute_script("arguments[0].click();", botao)
            time.sleep(3)
            
        except Exception as e:
            print("Não há mais botões para carregar.")
            break

finally:
    print("Processo finalizado.")
    navegador.quit()


with open('Atividades_FC.csv', mode='w', newline='', encoding='utf-8-sig') as csv_file:
    writer = csv.writer(csv_file, delimiter=';') # ; separa as colunas no excel br
    writer.writerow(['Nome', 'Categoria', 'Unidade', 'Data', 'Imagem', 'Descricao']) # Nomes das colunas
    writer.writerows(dados_list) # escreve as linhas