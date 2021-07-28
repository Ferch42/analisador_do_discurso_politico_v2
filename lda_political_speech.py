from nltk import word_tokenize
import os
import nltk
from tqdm import tqdm
from gensim import corpora
import pickle
import gensim
import string

import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


stop_words = nltk.corpus.stopwords.words('portuguese') + \
[punctuation for punctuation in string.punctuation] + \
["nº", "sobre", "lei", "art", "projeto", "votação", "emenda", "proposta", "requerimento"] + \
["comissão", "decreto", "nºs", "leis", "projetos", "emendas"] + \
["votações", "comissões", "orientação", "bancada", "mista", "orador"] + \
["medida", "provisória", "medidas", "provisórias", "questão", "ordem"] + \
["pauta", "pautas", "leitura", "discurso", "discussão", "§"] + \
["plenário", "pedido", "destaque", "separado", "artigo"]+ \
["anúncio", "solicitações", "solicitação"]

def tokenize(s):
	
	return [w for w in word_tokenize(s.lower()) if w not in stop_words]

def main():


	discursos_base_path = "./data/discursos/"
	discursos = os.listdir(discursos_base_path)

	corpus = []
	
	print('LOADING FILES')
	for d in tqdm(discursos):

		with open(os.path.join(discursos_base_path, d),  "r") as f:
			corpus += f.readlines()

	print("Tokenizing ")
	tokenized_corpus = [tokenize(c) for c in tqdm(corpus)]

	dictionary = corpora.Dictionary(tokenized_corpus)

	print('Transforming into bow')
	bow_corpus = [dictionary.doc2bow(text) for text in tqdm(tokenized_corpus)]

	NUM_TOPICS = 5
	try:
		os.mkdir(f"./models/{NUM_TOPICS}/")
	except:
		pass
	pickle.dump(bow_corpus, open(f"./models/{NUM_TOPICS}/corpus.pkl", 'wb'))
	dictionary.save(f"./models/{NUM_TOPICS}/dictionary.gensim")

	
	ldamodel = gensim.models.ldamodel.LdaModel(bow_corpus, num_topics = NUM_TOPICS, id2word=dictionary, passes = 15)
	ldamodel.save(f"./models/{NUM_TOPICS}/model.gensim")

	topics = ldamodel.print_topics(num_words=10)

	for t in topics:
		print(t)



if __name__ == '__main__':
	main()