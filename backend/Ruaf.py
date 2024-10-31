#librerias necesarias para el webscrapping
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json

#############################################

def cosnsultarRuaf():
    service = Service(ChromeDriverManager.install())
    option = webdriver.ChromeOptions()
    # mostrando pantalla del funcionamiento
    #option.add_argument("--window-size=1920,1080")
    #sin mostrar pantalla 
    option.add_argument("--headless") 
    #desabilita las extenciones (agiliza el funcionamiento)
    option.add_argument("--disable-extensions")
    driver= Chrome(service=service, options = option)
    #inicializar navegador

    tipoDocumento = 'cedula de ciudadania '
    cedula = 'cedula' #cedula a consultar
    fechaExpedicion = '12/05/2017'

    website = "https://ruaf.sispro.gov.co/TerminosCondiciones.aspx"# url
    driver.get(website)

    # click en aceptar terminos y en boton aceptar 
    respuesta = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH,"/html/body/div[9]/div/div/div/div[1]/div/div[1]/div/div/div/h3"))).text # validacion si la placa no tiene comparendos
    print(respuesta) # respuesta del servicio 
    
    time.sleep(20)