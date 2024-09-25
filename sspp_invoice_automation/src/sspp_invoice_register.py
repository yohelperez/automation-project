import time
import re
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from common.utils import perform_action_with_delay
from sspp_invoice_constants import EPM_REGISTER_INVOICE_URL

def extract_numbers(property_address):
    """
    Extract all numerical values from the given property address.

    Args:
        property_address (str): The address from which to extract numbers.

    Returns:
        list: A list of strings containing all the numbers found in the address.
    """
    return re.findall(r'\d+', property_address)

def select_matching_address(driver, property_address):
    """
    Select the address from the list that matches the provided property address.

    Args:
        driver (WebDriver): The Selenium WebDriver instance.
        property_address (str): The address to match against the list of available addresses.

    Returns:
        bool: True if a matching address was found and selected, otherwise False.
    """
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
    """
    Register a new invoice for a given contract and property address.

    Args:
        driver (WebDriver): The Selenium WebDriver instance.
        epm_contract_code (str): The contract code for which the invoice is being registered.
        property_address (str): The address associated with the property for the invoice.
    """
    driver.get(EPM_REGISTER_INVOICE_URL)
    
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