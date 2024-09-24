import subprocess
import time
import os
import requests
import random
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait, Select 
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

# run this line on cmd to open Chrome with remote debugging at port 9223: "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9223 --user-data-dir="C:\Temp\ChromeProfile9223"
# once it is done, this process can be run

chrome_executable = r"C:\Program Files\Google\Chrome\Application\chrome.exe" # Path to chrome executable 
user_data_dir = r"C:\Temp\ChromeProfile9223" # Path to chrome user profile
remote_debugging_port = "9223"
target_url = "https://www13.epm.com.co"
email = "perezyohel@gmail.com"
password = "Estranged98!"
download_path = "C:/Users/USUARIO/Documents/Automatizacion"

def perform_action_with_delay(action, *args, **kwargs):
    """Perform the given action with a random delay."""
    action(*args, **kwargs)
    time.sleep(random.uniform(1, 3)) 

def start_remote_chrome():
    """Start Chrome with remote debugging using subprocess."""
    command = [chrome_executable, f"--remote-debugging-port={remote_debugging_port}", f"--user-data-dir={user_data_dir}"]    
    subprocess.Popen(command)
    time.sleep(3) 

def initialize_driver():
    """Initialize Selenium to connect to a remote Chrome session and disable automation flags."""
    chrome_options = Options()

    chrome_options.add_experimental_option("debuggerAddress", f"127.0.0.1:{remote_debugging_port}") # Connect to remote debugging session
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")  # Disable AutomationControlled

    driver = webdriver.Chrome(options=chrome_options)
    
    return driver

def close_new_window(driver):
    """Detect and close the new window opened by the debugging command."""
    windows_before = set(driver.window_handles)
    start_remote_chrome()
    windows_after = set(driver.window_handles)

    if windows_before:
        new_window = windows_after - windows_before
        if new_window:
            new_window_handle  = new_window.pop()  # Obtains new window handle
            driver.switch_to.window(new_window_handle)
            driver.close()
            #driver.switch_to.window(windows_before[0])
            print(f"Nueva ventana detectada y cerrada: {new_window_handle}")

def find_window_by_url(driver):
    """Find a window by a specific URL."""
    print(f"handles: {driver.window_handles}")
    for handle in driver.window_handles:
        driver.switch_to.window(handle)
        print(f"Comparando: {driver.current_url} con {target_url}")
        if target_url in driver.current_url:
            return handle
    return None

def manage_window(driver):
    """Switch to the window with the target URL or open a new one if not found."""
    found_window = find_window_by_url(driver)

    if found_window:
        driver.switch_to.window(found_window)
        print(f"Ventana encontrada con la URL: {target_url}")
    else:
        print("No se encontró la ventana con la URL deseada. Abriendo una nueva ventana.")
        driver.get('https://www13.epm.com.co/FacturaWeb/Paginas/SesionIniciada.aspx')

def login(driver):
    """Log in to the website."""
    try:
        driver.get('https://www13.epm.com.co/FacturaWeb/Paginas/Inicio.aspx')
        email_field = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="ctl00_cphPrincipal_txtCorreo"]'))
        )
        email_field.send_keys(email)

        password_field = driver.find_element(By.XPATH, '//*[@id="ctl00_cphPrincipal_txtClave"]')
        password_field.send_keys(password)

        driver.find_element(By.XPATH, '//*[@id="ctl00_cphPrincipal_btnIngresar"]').click()
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="ctl00_cphPrincipal_lbVisualizadorHistorico"]'))
        )
        print("Inicio de sesión completado.")
        
    except TimeoutException:
        print("Error: El elemento esperado no apareció a tiempo. Verifique el proceso de inicio de sesión.")
        raise
    except Exception as e:
        print(f"Ocurrió un error durante el inicio de sesión: {e}")

def extract_numbers(property_address):
    # Expresión regular para extraer todos los números de la dirección
    return re.findall(r'\d+', property_address)

def select_matching_address(driver, property_address):
    property_address_numbers = extract_numbers(property_address)
    rows = driver.find_elements(By.XPATH, '//*[@id="ctl00_cphPrincipal_gveDirecciones"]/tbody/tr')

    for index, row in enumerate(rows, start=2):  # Index starts at 2 to match radio button ids
        address_element = row.find_element(By.XPATH, './td[2]')
        address_text = address_element.text.strip()

        address_numbers = extract_numbers(address_text)

        if address_numbers == property_address_numbers:
            radio_button_id = f'ctl00_cphPrincipal_gveDirecciones_ctl{index:02}_chkDireccion'
            radio_button = driver.find_element(By.ID, radio_button_id)
            time.sleep(1)
            radio_button.click()
            return True

    return False
        
def register_invoice(driver, epm_contract_code, property_address):
    """Register a new invoice."""
    #driver.find_element(By.XPATH, '//*[@id="ctl00_cphPrincipal_lbInscribirFacturas"]').click()
    driver.get('https://www13.epm.com.co/FacturaWeb/Paginas/InscribirFacturas.aspx')
    
    epm_contract_field = driver.find_element(By.XPATH, '//*[@id="ctl00_cphPrincipal_txtContrato"]')
    perform_action_with_delay(epm_contract_field.send_keys, epm_contract_code)
    
    # Click on "Inscribir factura"
    driver.find_element(By.XPATH, '//*[@id="ctl00_cphPrincipal_btnAdicionar"]').click()
    time.sleep(1)
    
    # Click on "Continuar"
    WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="ctl00_cphPrincipal_BtnContinuarValidacionCaptcha"]'))
    ).click()
    
    if select_matching_address(driver, property_address):
        driver.find_element(By.XPATH, '//*[@id="ctl00_cphPrincipal_btnGuardar"]').click()
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="ctl00_lblMasterPanel"]'))
        ).click()
        print(f"Resultado de la inscripción de la factura [{epm_contract_code}]: exitoso")
    else:
        print(f"Resultado de la inscripción de la factura [{epm_contract_code}]: fallido")

def search_contract_invoices(driver, epm_contract_code):
    """WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="ctl00_cphPrincipal_lbVisualizadorHistorico"]'))
    ).click()"""
    driver.get('https://www13.epm.com.co/FacturaWeb/Paginas/VisualizadorHistoricoFacturas.aspx')
    time.sleep(1) 
    
    # Click on select
    select_element = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, '//*[@id="ctl00_cphPrincipal_ddlContrato"]'))
    )
    select = Select(select_element)
    time.sleep(1) 
    select.select_by_value(epm_contract_code)
    
    driver.find_element(By.XPATH, '//*[@id="ctl00_cphPrincipal_btnConsultar"]').click() # Click on "Consultar"

def extract_invoice_pdf_url(driver):
    index = 2 
    img_pdf_element = None

    # Find the last pdf file
    while True:
        try:
            img_pdf_element = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, f'//*[@id="ctl00_cphPrincipal_grdHistorico_ctl{index:02}_imgPdf"]'))
            )
            index += 1  
        except TimeoutException:
            break

    if img_pdf_element:
        onclick_attr = img_pdf_element.get_attribute('onclick')

        # Extraemos la URL del PDF
        pdf_url_start = onclick_attr.find("'") + 1
        pdf_url_end = onclick_attr.rfind("'")
        pdf_url = onclick_attr[pdf_url_start:pdf_url_end]

        return pdf_url

    return None
    
def save_invoice_pdf(epm_contract_code, pdf_url):
    response = requests.get(pdf_url)

    if response.status_code == 200:
        if not os.path.exists(download_path):
                os.makedirs(download_path)
                
        save_path = os.path.join(download_path, f"factura_{epm_contract_code}.pdf")
        with open(save_path, "wb") as f:
            f.write(response.content)
        print(f"Archivo PDF guardado en: {save_path}")
    else:
        print(f"Error al descargar el PDF: {response.status_code}")
        
def download_invoice(driver, epm_contract_code):
    search_contract_invoices(driver, epm_contract_code)
    time.sleep(1) 
    pdf_url = extract_invoice_pdf_url(driver)
    time.sleep(1)
    if pdf_url:
        save_invoice_pdf(epm_contract_code, pdf_url)
    
def is_user_logged_in(driver): 
    try:
        driver.find_element(By.XPATH, '//*[@id="ctl00_lblNombre"]')
        return True
    except NoSuchElementException:
        return False
       
def main():
    """Main function to start sspp invoice register and download."""
    
    try:
        contract_code = "AD4878"
        epm_contract_code = "9524567"
        property_address = "CL 43 86 A 41 IN 301"
        
        # Initialize driver with remote connection
        driver = initialize_driver()
        
        # Close the new window opened by the debugging process
        close_new_window(driver)

        # Manage window or create a new one if it does not exist
        manage_window(driver)
        if is_user_logged_in(driver) == False:
            print("user not logged in, loging")
            login(driver)
            
        # Register invoice
        #register_invoice(driver, epm_contract_code, property_address)
        
        # Download invoice
        time.sleep(2) 
        download_invoice(driver, epm_contract_code)
        
        driver.quit()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
