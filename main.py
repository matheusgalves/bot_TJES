from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
import json
import os
import time
import re

caminho_arquivo = r'C:\\Users\\ntb_t\\OneDrive - TEAR\\Documentos\\projeto_andamentos\\bot_TJES\\teste.json'
link = 'http://aplicativos.tjes.jus.br/sistemaspublicos/consulta_12_instancias/consulta_proces.cfm'

with open(caminho_arquivo) as arquivo:
    dados = json.load(arquivo)

def proximoNup(indice_atual):
    indice = indice_atual + 1
    while indice < len(dados):
        if 'nup' in dados[indice]:
            return indice
        indice += 1
    return None

def abrirSite():
    nup = '0024856-21.2019.8.08.0048'
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get(link)
    time.sleep(5)
    janelas = driver.window_handles
    caixaNup = driver.find_element(By.XPATH, '/html/body/table/tbody/tr[2]/td/form/table/tbody/tr[5]/td/div[1]/table/tbody/tr[1]/td[2]/input')
    caixaNup.clear()
    caixaNup.send_keys(nup)
    select_instancia = Select(driver.find_element(By.ID, 'seInstancia'))
    select_instancia.select_by_value('2')
    driver.find_element(By.ID, 'buPesquisar').click()
    time.sleep(2)
    janelas = driver.window_handles
    driver.switch_to.window(janelas[1])
    processoNaoEncontrado = driver.find_elements(By.XPATH, "//td[@class='label_cons' and text()='Nenhum PROCESSO encontrado com os parâmetros informados.']")
    #primeira verificação = segunda instancia
    if processoNaoEncontrado:
        driver.switch_to.window(janelas[0])
        select_instancia = Select(driver.find_element(By.ID, 'seInstancia'))
        select_instancia.select_by_value('1')
        driver.find_element(By.ID, 'buPesquisar').click()
        time.sleep(2)
        janelas = driver.window_handles
        driver.switch_to.window(janelas[2])
        processoNaoEncontrado = driver.find_elements(By.XPATH, "//td[@class='label_cons' and text()='Nenhum PROCESSO encontrado com os parâmetros informados.']")
        # segunda verificaçao =  primeira instancia ==> justiça comum
        if processoNaoEncontrado:
            driver.switch_to.window(janelas[0])
            driver.find_element(By.XPATH, "//input[@name='seJuizo' and @value='2']").click()
            driver.find_element(By.ID, 'buPesquisar').click()
            time.sleep(2)
            janelas = driver.window_handles
            driver.switch_to.window(janelas[3])
            processoNaoEncontrado = driver.find_elements(By.XPATH, "//td[@class='label_cons' and text()='Nenhum PROCESSO encontrado com os parâmetros informados.']")
            # segunda verificaçao =  primeira instancia ==> juizado especial
            if processoNaoEncontrado:
                print("Processo Não Encontrado após as tentativas")
                    
            else: 
                linhas_andamentos = driver.find_elements(By.XPATH, "//tr[contains(@class, 'andamentos')]")
                datas_andamento = []

                for linha in linhas_andamentos:
                    spans_data = linha.find_elements(By.XPATH, ".//span[@style='font-weight:bold;' and @class='']")
                    # Se houver apenas um span de data, adiciona a data à lista
                    if len(spans_data) == 1:
                        data = spans_data[0].text.strip()
                        datas_andamento.append(data)

                # Imprime as datas coletadas para verificação (opcional)
                print(datas_andamento)
                textos_andamentos = []

                # Expressão regular para identificar a data no formato xx/xx/xxxx
                padrao_data = r"\b\d{2}/\d{2}/\d{4}\b"

                capturando_texto = False

                for linha in linhas_andamentos:
                    spans_data = linha.find_elements(By.XPATH, ".//span[@style='font-weight:bold;' and @class='']")
                    if len(spans_data) == 1:
                        capturando_texto = True
                    if capturando_texto:
                        conteudo_linha = linha.text.strip()
                        # Substituir a data encontrada na string por uma string vazia
                        texto_sem_data = re.sub(padrao_data, "", conteudo_linha, count= 1).strip()
                        if texto_sem_data:
                            textos_andamentos.append(texto_sem_data)

                # Imprime os textos capturados após as datas (opcional)
                print(textos_andamentos)
            
            # Agora, vamos capturar o texto das células após a coleta das datas
                
                formatoTabela = {
                                "Num Processo": nup,
                                "url": link,
                                "data_andamento": datas_andamento,
                                "texto_andamento": textos_andamentos,
                                }
                # Salva as datas em um arquivo JSON
                caminhoOutput = "C:\\Users\\ntb_t\OneDrive - TEAR\\Área de Trabalho\\git\\Tribunais-Project-Andamentos\\bot_TJES\\Output.json"

                with open(caminhoOutput, 'w', encoding='utf-8') as json_file:
                    json.dump(formatoTabela, json_file, indent=4, ensure_ascii=False)
        else: 
            datas_andamento = []
            ponto_referencia = driver.find_element(By.XPATH, "//td[@class='label_cons' and text()='Andamentos']")
            celulas_apos_referencia = ponto_referencia.find_elements(By.XPATH, "./following-sibling::td")
            for celula in celulas_apos_referencia:
                conteudo_celula = celula.text
                if '/' in conteudo_celula:
                    partes = conteudo_celula.split()
                    for parte in partes:
                        if '/' in parte:
                            data = parte
                            datas_andamento.append(data)
            
        
    else:
        datas_andamento = []
        ponto_referencia = driver.find_element(By.XPATH, "//td[@class='label_cons' and text()='Andamentos']")
        celulas_apos_referencia = ponto_referencia.find_elements(By.XPATH, "./following-sibling::td")
        for celula in celulas_apos_referencia:
            conteudo_celula = celula.text
            if '/' in conteudo_celula:
                partes = conteudo_celula.split()
                for parte in partes:
                    if '/' in parte:
                        data = parte
                        datas_andamento.append(data)
        with open ('Output.json', 'w') as json_file:
            json.dump(datas_andamento, json_file)

abrirSite()
#xx

# Itera sobre cada elemento 'nup' e realiza as verificações
#indice = 0
#while indice < len(dados):
   # if 'nup' in dados[indice]:
        #nup = dados[indice]['nup']
        #abrirSite(dados[indice])
        #proximo_indice = proximoNup(indice)
        #if proximo_indice is not None:
            #indice = proximo_indice
        #else:
            #break
    #indice += 1
