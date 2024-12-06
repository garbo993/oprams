#librerias necesarias para el webscrapping
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium_stealth import stealth
import time
import json

#############################################
#listas de datos #
basica = ["Cc","nombre1","nombre2", "apellido1", "apellido2","sexo"]
salud = ["afiliacion","regimen", "fechaAfiliacion","estado","tipoAfiliacion"]
pension = ["regimen","administradora","fechaAfiliacion","estadoAfiliacion"]
arl = ["admiministradora","fechaAfiliaicon","estado","actividadEconomica","municiopioLabora"]
compensacion = ["admiministradora","fechaAfiliaicon","estado","tipoMiembro","tipoAfiliado","municiopioLabora"]
#############################################

def convertirJson(lista, data):
    #covierte la respuesta de consulta de objeto de sesion selenium a lista#
    textos = [elemento.text  for elemento in data]
    texto = textos[0].split("\n")
    # une las listas de datos con los resultados de las consultas en un diccionario {key, value}#
    Dict = dict(zip(lista,texto))
    #print (Dict)
    #convierte el diccionario en JSON#
    info_json = json.dumps(Dict, ensure_ascii=False, indent=4)
    print(info_json)

###### Creacion de cliente de automatizador ##############

def cosnsultarRuaf(tipoDocumento,noDocumento,fechaExpedicion):
    #inicializar el servicio chrome automatizacion 
    service = Service(ChromeDriverManager().install())
    option = webdriver.ChromeOptions()
    # mostrando pantalla del funcionamiento
    #option.add_argument("--window-size=1920,1080")
    #sin mostrar pantalla 
    option.add_argument("--headless") 
    #desabilita las extenciones (agiliza el funcionamiento)
    option.add_argument("--disable-extensions")
    #desabilita el reconocimento de webdriver
    option.add_argument("--disable-blink-features-AutomationControlled")
    #desactiva los parametros de automatizacion para hacer pasar selenium como humano 
    option.add_experimental_option("excludeSwitches", ["enable-automation"])
    option.add_experimental_option('useAutomationExtension', False)
    driver= Chrome(service=service, options = option)

    #funcion que simula interfaz humana 
    stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
        )

##################################################   
    #inicializar navegador
    website = "https://ruaf.sispro.gov.co/TerminosCondiciones.aspx" # url
    driver.get(website)

    # click en aceptar terminos y en boton aceptar 

    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH,"/html/body/form/div[6]/div/table/tbody/tr[2]/td/table/tbody/tr[1]/td[2]/table/tbody/tr/td[1]/input"))).click() # click opcion aceptar
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH,"/html/body/form/div[6]/div/table/tbody/tr[2]/td/table/tbody/tr[2]/td[2]/input"))).click() # click continuar 
    
    #ingresar tipo de documento 

    DropdewonDocumento = Select(WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH,"/html/body/form/div[6]/div[1]/div/select"))))# buscar campo tipo de documento
    DropdewonDocumento.select_by_value(tipoDocumento)

    #ingresar cedula: 

    ccNumberInsert = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH,"/html/body/form/div[6]/div[2]/div/input"))) # buscar campo numero de cedula  
    ccNumberInsert.send_keys(noDocumento)
    
    #ingresar fecha en formato dd/mm/aaaa

    dateExpInsert = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH,"/html/body/form/div[6]/div[3]/div/input"))) # buscar campo  fecha de ex  pedicion  
    dateExpInsert.click()
    dateExpInsert.send_keys(fechaExpedicion)
    webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
    #time.sleep(5)
    
    #click boton consultar
    WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.XPATH,"/html/body/form/div[6]/div[4]/div/input"))).click() # click opcion aceptar

    #####################################################################
    #Obtener datos de ruaf 

    ####### informacion personal #############
    
    informacionPersonal = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.XPATH,"/html/body/form/div[6]/div[5]/div/div/table/tbody/tr[4]/td[3]/div/div[1]/div/table/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr[5]/td[3]/table/tbody/tr[3]")))
    # Extraer el texto de cada WebElement
    convertirJson(basica, informacionPersonal)

    ####### informacion de salud ############

    informacionSalud = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.XPATH,"/html/body/form/div[6]/div[5]/div/div/table/tbody/tr[4]/td[3]/div/div[1]/div/table/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr[10]/td[2]/table/tbody/tr[3]")))
    convertirJson(salud, informacionSalud)

    ####### Informacion pension ############

    informacionPension = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.XPATH,"/html/body/form/div[6]/div[5]/div/div/table/tbody/tr[4]/td[3]/div/div[1]/div/table/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr[17]/td[3]/table/tbody/tr[3]")))
    convertirJson(pension,informacionPension)

    ####### Informacion riesgos laborales  ############

    informacionArl = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.XPATH,"/html/body/form/div[6]/div[5]/div/div/table/tbody/tr[4]/td[3]/div/div[1]/div/table/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr[22]/td[3]/table/tbody/tr[3]")))
    convertirJson(arl,informacionArl)

    ####### Informacion Caja de compensacion  ############
    informacionCompensacion = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.XPATH,"/html/body/form/div[6]/div[5]/div/div/table/tbody/tr[4]/td[3]/div/div[1]/div/table/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr[27]/td[3]/table/tbody/tr[3]")))
    convertirJson(compensacion, informacionCompensacion)

    ###### Cesantias ###############
    informacionCesantias = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.XPATH,"/html/body/form/div[6]/div[5]/div/div/table/tbody/tr[4]/td[3]/div/div[1]/div/table/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr[34]")))
    

    time.sleep(20)
    driver.quit()


try:
    #parametros 
    tipoDocumento = '5|CC' # debe de ser #/siglas 5|CC cedula , 6|PA pasaporte, 7|AS ADULTO SIN IDENTIFICACION, 10|CD CARNET DIPLOMATICO, 12|CN CERTIFICADO DE NACIDO VIVO, 13|SC SALVACONDUCTO DE PERMANENCIA, 14|PE PERMISO ESPECIAL DE PERMANENCIA , 15|PT, PERMISO POR PROTECCION TEMPORAL, 1|MS MENOR SIN IDENTIFICACION,  2|RC  REGISTRO CIVIL , 3|TI  TARJETA DE IDENTIDAD,  4|CE  CEDULA DE EXTRANJERIA 
    noDocumento = 1023976157 #cedula a consultar
    fechaExpedicion = '12/05/2017' # fecha de expedicion de la cedula 
    cosnsultarRuaf(tipoDocumento,noDocumento,fechaExpedicion)
except:
    print ("No se pudo realizar la consulta")

