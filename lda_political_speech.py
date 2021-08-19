from nltk import word_tokenize
import os
import nltk
from tqdm import tqdm
from gensim import corpora
import pickle
import gensim
import string

import pyLDAvis
import pyLDAvis.gensim_models as gensimvis

from datetime import datetime
from dateutil.relativedelta import *
import pytz

from mockfirestore import MockFirestore

stop_words = nltk.corpus.stopwords.words('portuguese') + \
[punctuation for punctuation in string.punctuation] + \
["nºs", "nº", "§", "º", "i", 'ii', 'iii', "-a"] + \
["sobre", "lei", "art.", "projeto", "votação", "emenda", "proposta", "requerimento"] + \
["comissão", "decreto", "leis", "projetos", "emendas"] + \
["votações", "comissões", "orientação", "bancada", "mista", "orador"] + \
["medida", "provisória", "medidas", "provisórias", "questão", "ordem"] + \
["pauta", "pautas", "leitura", "discurso", "discussão"] + \
["plenário", "pedido", "destaque", "separado", "artigo"]+ \
["anúncio", "solicitações", "solicitação", "arts.", "inciso", "incisos"] + \
["caput", 'substitutivo', 'supressão', "assinaturas", "aprovação"] + \
["emissão", "parecer", "apresentação", "acerca", "apresentada"] + \
["apresentado", "submissão", 'transcurso', "congratulações"] + \
["homenagem", "alínea", "posicionamento", "regulamentação", "importância"]+ \
["necessidade", "declaração", "debate", "agradecimento", "oradora", "durante"] + \
['conversão', 'xii', 'constante', 'oferecido', 'oferecida', 'proposto', "contestação"] + \
['discursos', 'referente', 'art']
def tokenize(s):
	
	return [w for w in word_tokenize(s.lower()) if w not in stop_words]



from google.cloud import firestore
db_real = firestore.Client()

def main():

	# Transcurso
	db = MockFirestore()
	with open('./local_firestore.pkl', 'rb') as f:
		data = pickle.load(f)
	db._data = data

	brtz = pytz.timezone("Brazil/East")
	print("tokenizing")

	start_datetime = datetime(2019,2,1, tzinfo =brtz)

	while(start_datetime<datetime(2021,8,1, tzinfo =brtz)):

		query = db.collection('speeches').where("data", ">=", start_datetime).where('data', '<=', start_datetime +  relativedelta(months=+1)).stream()
		#query = db.collection('speeches').stream()
		tokenized_corpus = [tokenize(c.to_dict()['discurso_filtrado']) for c in tqdm(query)]

		if not tokenized_corpus:
			start_datetime = start_datetime +  relativedelta(months=+1)
			continue

		dictionary = corpora.Dictionary(tokenized_corpus)

		print('Transforming into bow')
		bow_corpus = [dictionary.doc2bow(text) for text in tqdm(tokenized_corpus)]

		NUM_TOPICS = 20
		try:
			os.mkdir(f"./models/{NUM_TOPICS}/")
		except:
			pass
		pickle.dump(bow_corpus, open(f"./models/{NUM_TOPICS}/corpus.pkl", 'wb'))
		dictionary.save(f"./models/{NUM_TOPICS}/dictionary.gensim")

		
		ldamodel = gensim.models.ldamodel.LdaModel(bow_corpus, num_topics = NUM_TOPICS, id2word=dictionary, passes=10, alpha = 'auto', eta = 'auto')
		ldamodel.save(f"./models/{NUM_TOPICS}/model.gensim")

		
		topics = ldamodel.print_topics(num_words=20)

		print("++++++++++++++++++++++++++++++++++++++++++")
		print(start_datetime)

		db_real.collection('topics').add({
				"data_inicio": start_datetime,
				"data_fim": start_datetime +  relativedelta(months=+1),
				"topics": [t[1] for t in topics]
			})

		for t in topics:
			print(t)

		start_datetime = start_datetime +  relativedelta(months=+1)
	#vis = gensimvis.prepare(ldamodel, bow_corpus, dictionary)
	#pyLDAvis.save_html(vis, 'index_lda.html')


if __name__ == '__main__':
	main()