from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

import time
from tqdm import tqdm
import json

# Start webdriver
options = Options()
driver = webdriver.Chrome("./chromedriver/windows/chromedriver.exe", options=options)

with open('./data/deputados.txt', 'r') as f:
	deputados = eval(f.read())


for dep in tqdm(deputados):
	
	driver.get("https://www2.camara.leg.br/atividade-legislativa/discursos-e-notas-taquigraficas")
	
	user = driver.find_element_by_name("txOrador")
	user.send_keys(dep)

	start_date = driver.find_element_by_name("dtInicio")
	start_date.send_keys("01/01/2018")
	submit_btn = driver.find_element_by_name("btnPesq")
	submit_btn.click()

	discursos_do_deputado = []

	try:
		WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="content"]/div/div[1]/div[2]/ul/li[2]/span')))
	
	except TimeoutException:

		not_found_speech = driver.find_element_by_xpath('//*[@id="content"]/div/p[1]/span')
		assert(not_found_speech.text == "Nenhum discurso encontrado.")
		print('Deputado sem discursos :', dep)
		
	try:
		while(True):
			expand_summary = driver.find_element_by_id("bnt-expand")
			expand_summary.click()
			a_tags = driver.find_elements_by_class_name('Sumario')

			discursos_do_deputado += [a.text + "\n" for a in a_tags]
			try: 
				prox_pag = driver.find_element_by_xpath('//*[@title="Próxima Página"]')
				prox_pag.click()
				WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="content"]/div/div[1]/div[2]/ul/li[2]/span')))

			except:
				break

	except:
		print('Deputado sem discursos :', dep)
	
	with open(f"./data/discursos/{dep.replace(' ', '_')}.txt", 'w+') as f:
		f.writelines(discursos_do_deputado)
