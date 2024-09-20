import requests
from bs4 import BeautifulSoup

url = 'https://www13.epm.com.co/FacturaWeb/Paginas/Inicio.aspx'

# Simular una sesión de navegador
session = requests.Session()
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
})

response = session.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')
    
    for link in soup.find_all('a'):
        print(link.get('href'))
else: 
    print(f'Error {response.status_code}')


'''
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC

chrome_options = Options()
# chrome_options.add_argument("--headless")  # sin ventana visible
chrome_options.add_experimental_option("detach", True)
chrome_options.add_argument("start-maximized")  # Maximizar la ventana
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)

# Remover 'navigator.webdriver' 
chrome_options.add_argument('--disable-blink-features=AutomationControlled')

driver = webdriver.Chrome(chrome_options)
driver.get('https://www13.epm.com.co/FacturaWeb/Paginas/Inicio.aspx') #https://google.com/recaptcha/api2/demo

try:
    email_field = WebDriverWait(driver, 30).until(
        EC.visibility_of_element_located((By.XPATH, '//*[@id="ctl00_cphPrincipal_txtCorreo"]'))
    )

    email_field.send_keys("perezyohel@gmail.com")
    
    password_field = driver.find_element(By.XPATH, '//*[@id="ctl00_cphPrincipal_txtClave"]')
    password_field.send_keys("Estranged98!")
    
    driver.find_element(By.XPATH, '//*[@id="ctl00_cphPrincipal_btnIngresar"]').click()

    # Aquí puedes añadir más interacciones, como enviar el formulario si es necesario
    # Por ejemplo: driver.find_element(By.XPATH, 'XPATH_DEL_BOTON_SUBMIT').click()

except Exception as e:
    print("Ocurrió un error:", e)

time.sleep(5)
#driver.switch_to.frame(0)
#driver.find_element(By.XPATH, '//*[@id="usYii7"]').click()

# WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, "iframe[id^='cf-chl-widget-']")))

# Esperar a que el elemento dentro del formulario esté visible y hacer clic en él
#captcha_element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@id='usYii7']")))
#captcha_element.click()


import re

def extract_numbers(address):
    # Usamos una expresión regular para extraer todos los números de la dirección
    numbers = re.findall(r'\d+', address)
    # Los convertimos en una lista de strings, separados por espacios para hacer la comparación más clara
    return ' '.join(numbers)

def compare_addresses(addr1, addr2):
    # Extraer los números de ambas direcciones
    numbers1 = extract_numbers(addr1)
    numbers2 = extract_numbers(addr2)
    
    # Comparar los números extraídos
    return numbers1 == numbers2

# Direcciones a comparar
address1 = "CL 43 CR 86 A -41 (INTERIOR 301 )"
address2 = "CL 43 86 A 41 IN 301"

# Comparar las direcciones
if compare_addresses(address1, address2):
    print("Las direcciones son equivalentes")
else:
    print("Las direcciones no son equivalentes")



'''