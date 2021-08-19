import re
import os
from tqdm import tqdm


regex_list = [r"(Orientação|Encaminhamento|Discussão|Emissão|Pedido|Agradecimento|Questão de ordem|Esclarecimento|Declaração|Defesa|Elogio|Apoio|Protesto).*?(sobre|acerca|respeito|para|referente)",\
r"(nº|n°)(s)? \d+\.?\d*",r"alteração da(s)? Lei(s)?", r"de \d+", r"(relativa|relativo) (à|ao|aos)", \
r"Apelo.*?(por|pelo|pela|a respeito|sobre|acerca|de)", r"art\. \d+º?\.?\d*", \
r"\d+\.?\d*(º|ª)?", r"arts\.", r"§", r"R$", r"%", r"(Apresentação|Aprovação).*?(de|da|do) ",\
r"votação em separado", r"Projeto de Lei", r"Medida Provisória", r"supressão", r"acerca", r"Decreto-Lei",\
r"revogação", r"Lei", r"dispositivo", r"destaques", r'destaque', r"ressalvado(s)?", r"ressalvada(s)?",\
r"inciso(s)?", r"redação", r'dada']

from google.cloud import firestore
db = firestore.Client()
# Transcurso

print("GETTING THE DATA")
data = db.collection('speeches').get()
print("DONE")
for speech in tqdm(data):

	speech_text = speech.to_dict()['discurso']

	clean_text = speech_text
	for r in regex_list:
		clean_text = re.sub(r, "", clean_text) 

	speech.reference.update({"discurso_filtrado": clean_text})

