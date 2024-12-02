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
basica = ["Cc","nombre1","nombre2", "apellido1", "apellido2","sexo"]
salud = ["afiliacion","regimen", "fechaAfiliacion","estado","tipoAfiliacion"]
pension = ["regimen","administradora","fechaAfiliacion","estadoAfiliacion"]
arl = ["admiminstradora","fechaAfiliaicon","estado","actividadEconomica","muiciopioLabora"]
conpensacion = ["admiminstradora","fechaAfiliaicon","estado","tipoMiembro","tipoAfiliado","muiciopioLabora"]

def response(data):
    Dict = dict.fromkeys(basica, data)
    print (Dict)
    datos_texto = {clave: [e.text for e in elementos] for clave, elementos in Dict.items()}
    print(datos_texto)

    datos_procesados = {}
    for clave, valor in datos_texto.items():
        partes = valor[0].split('\n')  # Dividir por saltos de línea
        datos_procesados['Cc'] = partes[0]
        datos_procesados['nombre1'] = partes[1]
        datos_procesados['nombre2'] = partes[2]
        datos_procesados['apellido1'] = partes[3]
        datos_procesados['apellido2'] = partes[4]
        datos_procesados['sexo'] = partes[5]
        break  # Evitar repetir el mismo procesamiento para cada campo

# Imprimir resultado
    print(datos_procesados)



'''
def convertJSON(consulta, data):
    i=0
    for  element in data :
        info_dict = {consulta[i]:element.text} # convierte la danta que entra(repuesta) a un diccionario
        i +=1 
        info_json = json.dumps(info_dict, ensure_ascii=False, indent=4) # convierte el diccionario en un Json para enviar al front
    print(info_json)
    return(info_json)  
'''     

###### Creacion de cliente de automatizador ##############

def cosnsultarRuaf():
    #inicializar el servicio chrome automatizacion 
    service = Service(ChromeDriverManager().install())
    option = webdriver.ChromeOptions()
    # mostrando pantalla del funcionamiento
    option.add_argument("--window-size=1920,1080")
    #sin mostrar pantalla 
    #option.add_argument("--headless") 
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

    #parametros 
    tipoDocumento = '5|CC' # debe de ser #/siglas 5|CC cedula , 6|PA pasaporte, 7|AS ADULTO SIN IDENTIFICACION, 10|CD CARNET DIPLOMATICO, 12|CN CERTIFICADO DE NACIDO VIVO, 13|SC SALVACONDUCTO DE PERMANENCIA, 14|PE PERMISO ESPECIAL DE PERMANENCIA , 15|PT, PERMISO POR PROTECCION TEMPORAL, 1|MS MENOR SIN IDENTIFICACION,  2|RC  REGISTRO CIVIL , 3|TI  TARJETA DE IDENTIDAD,  4|CE  CEDULA DE EXTRANJERIA 
    noDocumento = 1023976157 #cedula a consultar
    fechaExpedicion = '12/05/2017' # fecha de expedicion de la cedula 

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
    #response(informacionPersonal)
    # Extraer el texto de cada WebElement
    textos = [elemento.text  for elemento in informacionPersonal]
    texto = textos[0].split("\n")
    print(texto)

    # Imprimir los textos extraídos
    print(textos)

    #convertJSON(basica, informacionPersonal)

    ####### informacion de salud ############

    informacionSalud = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.XPATH,"/html/body/form/div[6]/div[5]/div/div/table/tbody/tr[4]/td[3]/div/div[1]/div/table/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr[10]/td[2]/table/tbody/tr[3]")))
    #response(informacionSalud)
    ####### Informacion pension ############

    informacionPension = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.XPATH,"/html/body/form/div[6]/div[5]/div/div/table/tbody/tr[4]/td[3]/div/div[1]/div/table/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr[17]/td[3]/table/tbody/tr[3]")))
    #response(informacionPension)
    ####### Informacion riesgos laborales  ############

    informacionArl = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.XPATH,"/html/body/form/div[6]/div[5]/div/div/table/tbody/tr[4]/td[3]/div/div[1]/div/table/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr[22]/td[3]/table/tbody/tr[3]")))
    #response(informacionArl)

    ####### Informacion Caja de compensacion  ############
    informacionCompensacion = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.XPATH,"/html/body/form/div[6]/div[5]/div/div/table/tbody/tr[4]/td[3]/div/div[1]/div/table/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr[27]/td[3]/table/tbody/tr[3]")))
    #response(informacionCompensacion)

    ###### Cesantias ###############

    informacionCesantias = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.XPATH,"/html/body/form/div[6]/div[5]/div/div/table/tbody/tr[4]/td[3]/div/div[1]/div/table/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr[34]")))
    #response(informacionCesantias)


    #####completa ############

    informacionCompleta = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.XPATH,"/html/body/form/div[6]/div[5]/div/div/table/tbody/tr[4]/td[3]/div/div[1]/div/table/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr/td/table")))
    #response(informacionCompleta)
    

    time.sleep(20)
    driver.quit()

cosnsultarRuaf()