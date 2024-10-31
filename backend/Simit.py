#librerias necesarias para el webscrapping
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

#############################################
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
    placa = 'abc123' #placa a ingresar 
    website = "https://www.fcm.org.co/simit/#/estado-cuenta?numDocPlacaProp="+ placa # url + la placa a imgresar
    driver.get(website)

    opcion = 0 
    try:
    # realiza la consulta buscando si no tiene comparendo con un tiempo de espera de 20 segundos 
        respuesta = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH,"/html/body/div[9]/div/div/div/div[1]/div/div[1]/div/div/div/h3"))) # validacion si la placa no tiene comparendos
        print(respuesta.text) # respuesta del servicio 

    except:
        # realiza la consulta buscando si tiene comparendos con un tiempo de espera de 20 segundos 
        respuesta = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH,"/html/body/div[9]/div/div/div/div[1]/div/div[1]/div[1]/div[1]"))) # validacion si la placa tiene comparendos
        print(respuesta.text) # respuesta del servicio 
    
    time.sleep(5)
    driver.quit()

ConsultaSimit()


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