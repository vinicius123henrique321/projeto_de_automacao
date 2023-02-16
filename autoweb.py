#OBJETIVO: importar uma base de dados e atualiza-la, recalcular os preços e exportar automaticamente#

### código de formatação ---> tabela = tabela.map('R${:.2f}'.format) 

# ter acessso a base de dados

import pandas as pd 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys 
import time

# criar o navegador
navegador = webdriver.Chrome()

# abrir o google
navegador.get("https://www.google.com.br/")

# digitar no navegador e encontrar a cotação do DÓLAR!
navegador.find_element('xpath', '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input').send_keys("cotação dólar")

navegador.find_element('xpath', '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input').send_keys(Keys.ENTER)

cotacao_dolar = navegador.find_element('xpath', '//*[@id="knowledge-currency__updatable-data-column"]/div[1]/div[2]/span[1]').get_attribute("data-value")

print(cotacao_dolar)

# EURO
navegador.get("https://www.google.com.br/")

navegador.find_element('xpath', '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input').send_keys("cotação do euro")

navegador.find_element('xpath', '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input').send_keys(Keys.ENTER)

cotacao_euro = navegador.find_element('xpath', '//*[@id="knowledge-currency__updatable-data-column"]/div[1]/div[2]/span[1]').get_attribute("data-value")

print(cotacao_euro)

# OURO
navegador.get("https://www.google.com.br/")

navegador.find_element('xpath', '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input').send_keys("cotação do ouro")

navegador.find_element('xpath', '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input').send_keys(Keys.ENTER)

navegador.get('https://www.melhorcambio.com/ouro-hoje')

cotacao_ouro = navegador.find_element('xpath', '//*[@id="comercial"]').get_attribute("value")

cotacao_ouro = cotacao_ouro.replace(",", ".")

print(cotacao_ouro)

# importar base de dados

base = pd.read_excel("Produtos.xlsx")

# atualizar a cotação

base.loc[base["Moeda"] == "Dólar", "Cotação"] = float(cotacao_dolar)
base.loc[base["Moeda"] == "Euro", "Cotação"] = float(cotacao_euro)
base.loc[base["Moeda"] == "Ouro", "Cotação"] = float(cotacao_ouro)

# recalcular os preços
# preço de compra = cotação * preço 

base["Preço de Compra"] = base["Cotação"] * base["Preço Original"]

# preço de venda = preço de compra * margem

base["Preço de Venda"] = base["Preço de Compra"] * base["Margem"]

base.to_excel("Produtos 2.xlsx", index=False)

