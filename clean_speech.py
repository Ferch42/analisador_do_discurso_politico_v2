import re
import os
from tqdm import tqdm


regex_list = [r"(Orientação|Encaminhamento|Discussão|Emissão|Pedido|Agradecimento|Questão de ordem|Esclarecimento|Declaração|Defesa|Elogio|Apoio|Protesto).*?(sobre|acerca|respeito|para|referente)",\
r"(nº|n°)(s)? \d+\.?\d*",r"alteração da(s)? Lei(s)?", r"de \d+", r"(relativa|relativo) (à|ao)", \
r"Apelo.*?(por|pelo|pela|a respeito|sobre|acerca|de)", r"art\. \d+º?\.?\d*", \
r"\d+\.?\d*(º|ª)?", r"arts\.", r"§", r"R$", r"%", r"(Apresentação|Aprovação).*?(de|da|do) ",\
r"votação em separado", r"Projeto de Lei", r"Medida Provisória"]

from google.cloud import firestore
db = firestore.Client()
# Transcurso

discurso_base_path = "./data/discursos/"

for file in tqdm(os.listdir(discurso_base_path)):

	with open(os.path.join(discurso_base_path, file), 'r') as f:

		lines = f.readlines()

	cleaned_lines = lines
	for r in regex_list:
		cleaned_lines = [re.sub(r, "", s) for s in cleaned_lines]

	with open(os.path.join("./data/discursos_cleaned/", file), 'w+') as g:

		g.writelines(cleaned_lines)
