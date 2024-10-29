
#librerias necesarias para el webscrapping
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

#############################################
from bs4 import BeautifulSoup
import requests
import time

#opciones de navegacion 
def main():
    service=Service(ChromeDriverManager().install())
    option = webdriver.ChromeOptions()
    # mostrando pantalla del funcionamiento
    option.add_argument("--window-size=1920,1080")
    #sin mostrar pantalla 
    #options.add_argument("--headless") 
    #   option.add_argument("--disable-extensions")
    driver= Chrome(service=service, options = option)
    #inicializar navegador
    placa = 'abc123'
    website = "https://www.fcm.org.co/simit/#/estado-cuenta?numDocPlacaProp="+ placa
    driver.get(website)
    time.sleep(20)
    respuesta1 = driver.find_element(By.CLASS_NAME, 'mb-0 fs-17 font-weight-bold text-secondary')
    respuesta2 = driver.find_element(By.CLASS_NAME, 'card bg-estado-section border-0 box-shadow-sm"')
    print(respuesta1.text)
    print(respuesta2.text)
    time.sleep(20)
    driver.quit()
main()


#if __name__ =="__main__ ":
#    main()






''''
# ingreso de placa y url de la pagina 
placa = 'gqt188'
website = 'https://www.fcm.org.co/simit/#/estado-cuenta?numDocPlacaProp=gqt188'

time.sleep(20)
# response realiza la peticion get a la pagina web 
response =  requests.get(website)
# obtiene el html de la pagina
content = response.text 

# 
soup = BeautifulSoup(content, 'html.parcer')
#print(soup.prettify())

box = soup.find('p', class_= 'mb-0 fs-17 font-weight-bold text-secondary' )
print(box)

'''