from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

options = Options()

driver = webdriver.Chrome("./chromedriver/windows/chromedriver.exe", options=options)
driver.get("https://www2.camara.leg.br/atividade-legislativa/discursos-e-notas-taquigraficas")
user = driver.find_element_by_name("txOrador")
user.send_keys("Tabata Amaral")

submit_btn = driver.find_element_by_name("btnPesq")
submit_btn.click()
time.sleep(2)
a_tags = driver.find_element_by_xpath('//table/tbody/tr[2]/td/a')
a_tags.click()