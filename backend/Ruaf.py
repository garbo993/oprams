## librerias necesarias para el webscrapping ##
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium_stealth import stealth
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
import time

#############################################

# listas de datos #
basica = ["Cc","nombre1","nombre2", "apellido1", "apellido2","sexo"]
salud = ["afiliacion","regimen", "fechaAfiliacion","estado","tipoAfiliacion"]
pension = ["regimen","administradora","fechaAfiliacion","estadoAfiliacion"]
arl = ["admiministradora","fechaAfiliaicon","estado","actividadEconomica","municiopioLabora"]
compensacion = ["admiministradora","fechaAfiliaicon","estado","tipoMiembro","tipoAfiliado","municiopioLabora"]

#############################################

def convertirJson(lista, data):
    ### covierte la respuesta de consulta de objeto de sesion selenium a lista ###
    textos = [elemento.text  for elemento in data]
    ### separa el .text de cadena conjunta  a separada por "\n" para ingresarlas al diccionario y asignarlas ###
    texto = textos[0].split("\n")
    ### une las listas de datos con los resultados de las consultas en un diccionario {key, value} ###
    Dict = dict(zip(lista,texto))
    ### retorna el diccionario unido para mandar la respuesta de api ###
    #print (Dict) # debugg #
    return Dict

# Creacion de cliente de automatizador #

def consultarRuaf(tipoDocumento,noDocumento,fechaExpedicion):

    ## convierte la fecha ingresada de dd-mm-aaaa en dd/mm/aaaa ##

    fechaExpedicion = fechaExpedicion.replace("-","/" )

    #inicializar el servicio chrome automatizacion 

    service = Service(ChromeDriverManager().install())
    option = webdriver.ChromeOptions()

    ### mostrando pantalla del funcionamiento ###

    #option.add_argument("--window-size=1920,1080")

    ###sin mostrar pantalla ###

    option.add_argument("--headless") 

    ### desabilita las extenciones (agiliza el funcionamiento) ###

    option.add_argument("--disable-extensions")

    ### desabilita el reconocimento de webdriver ###

    option.add_argument("--disable-blink-features-AutomationControlled")

    ### desactiva los parametros de automatizacion para hacer pasar selenium como humano ###

    option.add_experimental_option("excludeSwitches", ["enable-automation"])
    option.add_experimental_option('useAutomationExtension', False)
    driver= Chrome(service=service, options = option)

    ## funcion que simula interfaz humana ##
    stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
        )

################################################################

    # ejecucion del servicio #
   
    ### inicializar navegador ###
    website = "https://ruaf.sispro.gov.co/TerminosCondiciones.aspx" # url
    driver.get(website)

    ### click en aceptar terminos y en boton aceptar ###

    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH,"/html/body/form/div[6]/div/table/tbody/tr[2]/td/table/tbody/tr[1]/td[2]/table/tbody/tr/td[1]/input"))).click() # click opcion aceptar
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH,"/html/body/form/div[6]/div/table/tbody/tr[2]/td/table/tbody/tr[2]/td[2]/input"))).click() # click continuar 
    
    ###ingresar tipo de documento ###

    DropdewonDocumento = Select(WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH,"/html/body/form/div[6]/div[1]/div/select"))))# buscar campo tipo de documento
    DropdewonDocumento.select_by_value(tipoDocumento)

    ###ingresar cedula: ###

    ccNumberInsert = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH,"/html/body/form/div[6]/div[2]/div/input"))) # buscar campo numero de cedula  
    ccNumberInsert.send_keys(noDocumento)
    
    ### ingresar fecha en formato dd/mm/aaaa ###

    dateExpInsert = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH,"/html/body/form/div[6]/div[3]/div/input"))) # buscar campo  fecha de ex  pedicion  
    dateExpInsert.click()
    dateExpInsert.send_keys(fechaExpedicion)
    webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()

    #time.sleep(5) ### activar si la ventana no esta detectando los campos de peticion ###
    
    ### click boton consultar ###

    WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.XPATH,"/html/body/form/div[6]/div[4]/div/input"))).click() # click opcion aceptar

    #####################################################################

    # obtencion de datos #
    time.sleep(5)
    ### Dicicionario de respuesta ###

    response = {}

    # como funciona #

    '''
    en los parametrso de informacion lo que el algoritmo hace es un proceso de 3 fases 

    ## primera fase ##
    try:
        informacion = busca hasta un tiempo de 20 la ruta xpath asignada 
        response  = crea el diccionario en donde se almacena la data tomada de informacion ejecutando la funcion convertirJson para transformar la data de objeto a texto
          {
                    tipoInfo = convertirJson()
        }
    ## segunda fase ## 
    except TimeoutException: ### en el caso de no encontrar el xpath mencionado en el tiempo establecido retornara a este except ###
        response = {tipoInfo = " excepcion "}
    
    ## tercera fase ## 
    except StaleElementReferenceException: ### esta excepcion se ejecuta cuando el xpath no se encunetra dentro del DOM de la pagina ### 
        print("El elemento ya no está adjunto al DOM.")
        ### no retorna nada debido a que es un problema de DOM de la pagina, si ocurre debe de comprobarse el estado de la pagina y si cambio su DOM  ###


    '''

    # captura de la informacion #

    ## informacion personal ##
    try:
        informacionPersonal = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.XPATH,"/html/body/form/div[6]/div[5]/div/div/table/tbody/tr[4]/td[3]/div/div[1]/div/table/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr[5]/td[3]/table/tbody/tr[3]")))
        response = dict(response ,  informacionPersonal  = convertirJson(basica, informacionPersonal))

    except TimeoutException:
        response = dict(response ,  informacionPersonal  = "no hay registro")
        print("No se encontró el elemento en el tiempo esperado.")

    except StaleElementReferenceException:
        print("El elemento ya no está adjunto al DOM.")
    
    
    ## informacion de salud ##
    try:
        informacionSalud = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.XPATH,"/html/body/form/div[6]/div[5]/div/div/table/tbody/tr[4]/td[3]/div/div[1]/div/table/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr[10]/td[2]/table/tbody/tr[3]")))
        response = dict(response ,  informacionSalud = convertirJson(salud, informacionSalud))
    
    except TimeoutException:
        response = dict(response ,  informacionSalud  = "no hay registro")
        print("No se encontró el elemento en el tiempo esperado.")
    
    except StaleElementReferenceException:
        print("El elemento ya no está adjunto al DOM.")


    ## Informacion pension ##
    try:
        informacionPension = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.XPATH,"/html/body/form/div[6]/div[5]/div/div/table/tbody/tr[4]/td[3]/div/div[1]/div/table/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr[17]/td[3]/table/tbody/tr[3]")))
        response = dict(response ,  informacionPension = convertirJson(pension,informacionPension))

    except TimeoutException:
        response = dict(response ,  informacionSalud  = "no hay registro")
        print("No se encontró el elemento en el tiempo esperado.")
    
    except StaleElementReferenceException:
        print("El elemento ya no está adjunto al DOM.")
    
    ## Informacion riesgos laborales  ##
    try:
        informacionArl = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.XPATH,"/html/body/form/div[6]/div[5]/div/div/table/tbody/tr[4]/td[3]/div/div[1]/div/table/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr[22]/td[3]/table/tbody/tr[3]")))
        response = dict(response ,  informacionArl =convertirJson(arl,informacionArl))

    except TimeoutException:
        response = dict(response ,  informacionArl  = "no hay registro")
        print("No se encontró el elemento en el tiempo esperado.")

    except StaleElementReferenceException:
        print("El elemento ya no está adjunto al DOM.")

    
    ## Informacion Caja de compensacion  ##
    try:
        informacionCompensacion = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.XPATH,"/html/body/form/div[6]/div[5]/div/div/table/tbody/tr[4]/td[3]/div/div[1]/div/table/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr[27]/td[3]/table/tbody/tr[3]")))
        response = dict(response ,   informacionCompensacion = convertirJson(compensacion, informacionCompensacion))

    except TimeoutException:
        response = dict(response ,  informacionCompensacion  = "no hay registro")
        print("No se encontró el elemento en el tiempo esperado.")

    except StaleElementReferenceException:
        print("El elemento ya no está adjunto al DOM.")


    ## Cesantias ##
    #informacionCesantias = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.XPATH,"/html/body/form/div[6]/div[5]/div/div/table/tbody/tr[4]/td[3]/div/div[1]/div/table/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr[34]")))
   
    ### espera de tiempo para capturar la data ###

    time.sleep(20)
    driver.quit() ## cierra el navegador ##

    # respuesta del servicio #
    return  response



# parametros de prueba del servicio #

'''    
try:
    #parametros 
    tipoDocumento = '5|CC' # debe de ser #/siglas 5|CC cedula , 6|PA pasaporte, 7|AS ADULTO SIN IDENTIFICACION, 10|CD CARNET DIPLOMATICO, 12|CN CERTIFICADO DE NACIDO VIVO, 13|SC SALVACONDUCTO DE PERMANENCIA, 14|PE PERMISO ESPECIAL DE PERMANENCIA , 15|PT, PERMISO POR PROTECCION TEMPORAL, 1|MS MENOR SIN IDENTIFICACION,  2|RC  REGISTRO CIVIL , 3|TI  TARJETA DE IDENTIDAD,  4|CE  CEDULA DE EXTRANJERIA 
    noDocumento = 123456 #cedula a consultar
    fechaExpedicion = 'dd-mm-aaaa'# fecha de expedicion de la cedula 

    consultarRuaf(tipoDocumento,noDocumento,fechaExpedicion)

except:
    print ("No se pudo realizar la consulta")

'''