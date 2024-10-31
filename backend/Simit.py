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
    if "no tienes comparendos ni multas registradas en simit" in data.lower():
        info_dict = {"comparendos": "No tienes comparendos ni multas registradas en Simit"}
        
    else:

        lines = data.strip().split("\n")[1:]
        # Creamos un diccionario a partir de las líneas
        info_dict = {}
        for line in lines:
            key, value = line.split(": ")
            info_dict[key.strip()] = value.strip()

    # Convertimos el diccionario a JSON
    info_json = json.dumps(info_dict, ensure_ascii=False, indent=4)
    print(info_json)

###################################################

#opciones de navegacion 
def ConsultaSimit():
    service=Service(ChromeDriverManager().install())
    option = webdriver.ChromeOptions()
    # mostrando pantalla del funcionamiento
    #option.add_argument("--window-size=1920,1080")
    #sin mostrar pantalla 
    option.add_argument("--headless") 
    #desabilita las extenciones (agiliza el funcionamiento)
    option.add_argument("--disable-extensions")
    driver= Chrome(service=service, options = option)
    #inicializar navegador
    placa = 'gqt188' #placa a ingresar 
    website = "https://www.fcm.org.co/simit/#/estado-cuenta?numDocPlacaProp="+ placa # url + la placa a imgresar
    driver.get(website)
    # try catch dependiendo de si tiene o no comparendos 
    try:
    # realiza la consulta buscando si no tiene comparendo con un tiempo de espera de 20 segundos 
        respuesta = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH,"/html/body/div[9]/div/div/div/div[1]/div/div[1]/div/div/div/h3"))).text # validacion si la placa no tiene comparendos
        print(respuesta) # respuesta del servicio 

    except:
        # realiza la consulta buscando si tiene comparendos con un tiempo de espera de 20 segundos 
        respuesta = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH,"/html/body/div[9]/div/div/div/div[1]/div/div[1]/div[1]/div[1]"))).text # validacion si la placa tiene comparendos
        print(respuesta) # respuesta del servicio 
        
    convertir_a_Json(respuesta)
    time.sleep(5)
    driver.quit()

#ejecucion de funcion 
ConsultaSimit()
#if __name__ =="__main__ ":
#    main()
