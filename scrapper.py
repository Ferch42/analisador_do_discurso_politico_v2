import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
import json

r = requests.get("https://www.camara.leg.br/internet/agencia/infograficos-html5/DeputadosEleitos/index.html")

tabela_deputados = pd.read_html(r.text)[0]

estados = {}
deputados = []

for i,row in tabela_deputados.iterrows():

	if row['Nome'] == row['Partido']:
		# novo estado
		estado = row['Nome']
		continue
	deputados.append({'nome': row['Nome'],
					'partido': row['Partido'],
					'estado': estado})

f = open('./data/deputados.json', "w+")

f.write(json.dumps(deputados).replace('}', '}\n'))
f.close()