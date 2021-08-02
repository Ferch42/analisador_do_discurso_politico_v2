from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

from google.cloud import firestore
import time
from tqdm import tqdm
import json
from datetime import datetime

# Start webdriver
options = Options()
driver = webdriver.Chrome("./chromedriver/windows/chromedriver.exe", options=options)
db = firestore.Client()
driver.implicitly_wait(1) 

with open('./data/deputados.txt', 'r') as f:
	deputados = eval(f.read())


for dep in tqdm(deputados):
	
	driver.get("https://www2.camara.leg.br/atividade-legislativa/discursos-e-notas-taquigraficas")
	
	user = driver.find_element_by_name("txOrador")
	user.send_keys(dep)

	start_date = driver.find_element_by_name("dtInicio")
	start_date.send_keys("01/01/2019")
	submit_btn = driver.find_element_by_name("btnPesq")
	submit_btn.click()

	discursos_do_deputado = []

	try:
		WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, '//*[@id="content"]/div/div[1]/div[2]/ul/li[2]/span')))
	
	except TimeoutException:

		not_found_speech = driver.find_element_by_xpath('//*[@id="content"]/div/p[1]/span')
		assert(not_found_speech.text == "Nenhum discurso encontrado.")
		print('Deputado sem discursos :', dep)
		
	try:
		while(True):
			expand_summary = driver.find_element_by_id("bnt-expand")
			expand_summary.click()
			a_tags = driver.find_elements_by_class_name('Sumario')
			
			#discursos_do_deputado += [a.text + "\n" for a in a_tags]
			
			discursos = [a.text for a in a_tags]
			# Extracts the dates from the site
			c = 1
			dates = []
			while(True):
				try:
					date = driver.find_element_by_xpath(f'//*[@id="content"]/div/table/tbody/tr[{c}]/td[1]')
					dates.append(date.text)
					c+=2
				except:
					break

			assert(len(dates) == len(discursos))
			for discurso, data in zip(discursos, dates):

				discurso_dict = {'deputado':dep, 'discurso': discurso, 'data': datetime.strptime(data,"%d/%m/%Y") }
				discursos_do_deputado.append(discurso_dict)
				db.collection('speeches').add(discurso_dict)
			try: 
				prox_pag = driver.find_element_by_xpath('//*[@title="Próxima Página"]')
				prox_pag.click()
				WebDriverWait(driver,60).until(EC.presence_of_element_located((By.XPATH, '//*[@id="content"]/div/div[1]/div[2]/ul/li[2]/span')))

			except:
				break

	except:
		print('Deputado sem discursos :', dep)
	
	with open(f"./data/discursos/{dep.replace(' ', '_')}.txt", 'w+') as f:
		f.write(str(discursos_do_deputado))
