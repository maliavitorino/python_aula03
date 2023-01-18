#!/usr/bin/env python
# coding: utf-8

# In[7]:


get_ipython().system('pip install selenium')


# In[22]:


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

# Passo 1: Pegar a cotação do dólar

# entrar no google
navegador = webdriver.Chrome()
navegador.get("https://www.google.com/")

navegador.find_element('xpath', '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input').send_keys("cotação dólar")
navegador.find_element('xpath', '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input').send_keys(Keys.ENTER)

# pegar o valor

cotacao_dolar = navegador.find_element('xpath', '//*[@id="knowledge-currency__updatable-data-column"]/div[1]/div[2]/span[1]').get_attribute('data-value')

# Passo 2: Pegar a cotação do euro

navegador.get("https://www.google.com/")
navegador.find_element('xpath', '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input').send_keys("cotação euro")
navegador.find_element('xpath', '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input').send_keys(Keys.ENTER)

# pegar o valor

cotacao_euro = navegador.find_element('xpath', '//*[@id="knowledge-currency__updatable-data-column"]/div[1]/div[2]/span[1]').get_attribute('data-value')

# Passo 3: Pegar a cotação do ouro

navegador.get("https://www.melhorcambio.com/ouro-hoje")
cotacao_ouro = navegador.find_element('xpath', '//*[@id="comercial"]').get_attribute('value')
cotacao_ouro = cotacao_ouro.replace(",", ".")

navegador.quit()

print(cotacao_dolar)
print(cotacao_euro)
print(cotacao_ouro)

# Passo 4: Importar a base de dados e Atualizar a base

import pandas as pd

tabela = pd.read_excel("Produtos.xlsx")

# Passo 5: Recalcular os preços
# atualizar cotação
#cotação dolar

tabela.loc[tabela["Moeda"] == "Dólar", "Cotação"] = float(cotacao_dolar)

#cotação euro

tabela.loc[tabela["Moeda"] == "Euro", "Cotação"] = float(cotacao_euro)

#cotação ouro

tabela.loc[tabela["Moeda"] == "Ouro", "Cotação"] = float(cotacao_ouro)

# recalcular os preços
# preço de compra = cotação * preço original

tabela["Preço de Compra"] = tabela["Cotação"] * tabela["Preço Original"]

# preço de venda = preço de compra * margem

tabela["Preço de Venda"] = tabela["Preço de Compra"] * tabela["Margem"]

# formatar no excel para não perder a exatidão do valores
# Passo 6: Exportar a base atualizada

tabela.to_excel("Produtos Atualizado.xlsx", index=False)

display(tabela)


# In[ ]:




