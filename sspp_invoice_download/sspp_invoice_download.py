import subprocess
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait, Select 
from selenium.webdriver.support import expected_conditions as EC


# correr esta linea en consola para abrir el navegador con el puerto 9223: "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9223 --user-data-dir="C:\Temp\ChromeProfile"

# o alternativamente automatizarlo para que lo abra solo
# Ruta al ejecutable de Chrome y al perfil de usuario
chrome_executable = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
user_data_dir = r"C:\Temp\ChromeProfile"


def start_remote_chrome(chrome_executable, user_data_dir):
    """Start Chrome with remote debugging using subprocess."""
    command = [chrome_executable, "--remote-debugging-port=9223", f"--user-data-dir={user_data_dir}"]    
    subprocess.Popen(command)
    time.sleep(3) 

def initialize_driver():
    """Initialize Selenium to connect to a remote Chrome session."""
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9223")  # Connects to chrome session
    return webdriver.Chrome(options=chrome_options)

def close_new_window(driver):
    """Detect and close the new window opened by the debugging command."""
    windows_before = set(driver.window_handles)
    start_remote_chrome(chrome_executable, user_data_dir)
    windows_after = set(driver.window_handles)

    if windows_before:
        new_window = windows_after - windows_before
        if new_window:
            new_window_handle  = new_window.pop()  # Obtener el handle de la nueva ventana
            driver.switch_to.window(new_window_handle)
            driver.close()
            print(f"Nueva ventana detectada y cerrada: {new_window_handle}")

def find_window_by_url(driver, target_url):
    """Find a window by a specific URL."""
    for handle in driver.window_handles:
        driver.switch_to.window(handle)
        if target_url in driver.current_url:
            return handle
    return None

def manage_window(driver, target_url):
    """Switch to the window with the target URL or open a new one if not found."""
    found_window = find_window_by_url(driver, target_url)

    if found_window:
        driver.switch_to.window(found_window)
        print(f"Ventana encontrada con la URL: {target_url}")
    else:
        print("No se encontró la ventana con la URL deseada. Abriendo una nueva ventana.")
        driver.get('https://www13.epm.com.co/FacturaWeb/Paginas/Inicio.aspx')

def login(driver, email, password):
    """Log in to the website."""
    try:
        email_field = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="ctl00_cphPrincipal_txtCorreo"]'))
        )
        email_field.send_keys(email)

        password_field = driver.find_element(By.XPATH, '//*[@id="ctl00_cphPrincipal_txtClave"]')
        password_field.send_keys(password)

        driver.find_element(By.XPATH, '//*[@id="ctl00_cphPrincipal_btnIngresar"]').click()
        print("Inicio de sesión completado.")

    except Exception as e:
        print(f"Ocurrió un error durante el inicio de sesión: {e}")
        
def register_invoice(driver, epm_contract_code, property_address):
    """Register a new invoice."""
    driver.find_element(By.XPATH, '//*[@id="ctl00_cphPrincipal_lbInscribirFacturas"]').click()
    
    epm_contract_field = driver.find_element(By.XPATH, '//*[@id="ctl00_cphPrincipal_txtContrato"]')
    epm_contract_field.send_keys(epm_contract_code)
    
    # Click on "Inscribir factura"
    driver.find_element(By.XPATH, '//*[@id="ctl00_cphPrincipal_btnAdicionar"]').click()
    
    # Click on "Continuar"
    WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="ctl00_cphPrincipal_BtnContinuarValidacionCaptcha"]'))
    ).click()
    
    # to do: compare addresses 
    # click on "Guardar cambios": XPATH: //*[@id="ctl00_cphPrincipal_btnGuardar"]
    # click on "Cerrar": XPATH: //*[@id="ctl00_lblMasterPanel"]
    
def download_invoice(driver, epm_contract_code):
    
    # Click on "Ver historico"
    WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="ctl00_cphPrincipal_lbVisualizadorHistorico"]'))
    ).click()
    
    select_element = driver.find_element(By.XPATH, '//*[@id="ctl00_cphPrincipal_ddlContrato"]')
    
    # Crear un objeto Select para interactuar con el select
    select = Select(select_element)
    
    # Seleccionar la opción por value
    select.select_by_value(epm_contract_code)
    
    driver.find_element(By.XPATH, '//*[@id="ctl00_cphPrincipal_btnConsultar"]').click()
    
    WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="ctl00_cphPrincipal_grdHistorico_ctl07_imgPdf"]'))
    ).click()
    
    pdf_download_url = "https://facturawebepm.cadenaportalgestion.com/"
    for handle in driver.window_handles:
        driver.switch_to.window(handle)
        if pdf_download_url in driver.current_url:
            break
        
    # to do: click on download 
    
def main():
    """Main function to start sspp invoice download."""
    
    target_url = "https://www13.epm.com.co"
    email = "perezyohel@gmail.com"
    password = "Estranged98!"
    contract_code = "AD4878"
    epm_contract_code = "9524567"
    property_address = "CL 43 86 A 41 IN 301"
    
    
    # Initialize driver with remote connection
    driver = initialize_driver()
    #initial_window = driver.current_window_handle

    # Close the new window opened by the debugging process
    close_new_window(driver)

    # Manage window or create a new one if it does not exist
    manage_window(driver, target_url)

    # Perform login
    login(driver, email, password)

    # Register invoice
    #registerInvoice(driver, epm_contract_code, property_address)
    
    # Download invoice
    download_invoice(driver, epm_contract_code)
    
    driver.quit()


if __name__ == "__main__":
    main()
