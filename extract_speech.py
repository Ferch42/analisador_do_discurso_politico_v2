from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from tqdm import tqdm
import json

# Start webdriver
options = Options()
driver = webdriver.Chrome("./chromedriver/windows/chromedriver.exe", options=options)

with open('./data/deputados.txt', 'r') as f:
	deputados = eval(f.read())


for dep in deputados:
	
	driver.get("https://www.camara.leg.br/deputados/quem-sao")
	name_field = driver.find_element_by_xpath('//*[@id="main-content"]/section/div/div[1]/form/span/input')
	name_field.send_keys(dep)

	time.sleep(1.5)
	autocomplete_find = driver.find_element_by_xpath("//body/ul/li[1]")
	autocomplete_find.click()

	search_btn = driver.find_element_by_xpath('//*[@id="main-content"]/section/div/div[1]/form/div/button')
	search_btn.click()


	time.sleep(8)

	print("deputado: ", dep)
	try:
		discursos_dados = driver.find_element_by_xpath('//*[@id="atuacao-section"]/div[1]/div[3]/div/div[2]/div/div/span[2]')
														
		print("Numero de discursos dados", discursos_dados.text)

	except: 
		discursos_dados = driver.find_element_by_xpath('//*[@id="atuacao-section"]/div[1]/div[3]/div/div[2]/div/div/a')
		print("Numero de discursos dados", discursos_dados.text)
