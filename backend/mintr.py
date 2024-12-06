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


def convertir_a_Json(data):
    info_dict = {"consulta": data} # convierte la data que entra(repuesta) a un diccionario
    #info_json = json.dumps(info_dict, ensure_ascii=False, indent=4) # convierte el diccionario en un Json para enviar al front
    #print(info_json)
    #return(info_json)
    return info_dict
#############################################

def consultarMintri(placa):
        service = Service(ChromeDriverManager().install())
        option = webdriver.ChromeOptions()
        # mostrando pantalla del funcionamiento
        #option.add_argument("--window-size=1920,1080")
        #sin mostrar pantalla 
        option.add_argument("--headless") 
        #desabilita las extenciones (agiliza el funcionamiento)
        option.add_argument("--disable-extensions")
        driver= Chrome(service=service, options = option)
        #inicializar navegador
        
        #placa a ingresar 

        website = "https://normalizacion.mintransporte.gov.co/?placa=" + placa.upper() # envia el numero de placa en mayuscula 
        driver.get(website)

        #realiza la consulta si tiene o no problemas en su registro de matricula 
        respuesta = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH,"/html/body/div[2]"))).text # validacion si la placa no tiene comparendos

        ####termina la ejecucion####
        time.sleep(5)
        driver.quit()
        return convertir_a_Json(respuesta) # respuesta del servicio 
        

'''
try:    
        #placa = "KUK472"
        #consultarMintri(placa) # ejecuta la funcion 
        
except:
        respuesta = "el servidor no responde" 
        print(respuesta)

'''
