import time
import os
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select 
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from sspp_invoice_constants import EPM_HISTORICAL_URL, INVOICE_DOWNLOAD_PATH

def search_contract_invoices(driver, epm_contract_code):
    """
    Navigate to the historical invoices page and search for invoices related to a specific contract.

    Args:
        driver (WebDriver): The Selenium WebDriver instance.
        epm_contract_code (str): The contract code for which invoices will be searched.
    """
    driver.get(EPM_HISTORICAL_URL)
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
    """
    Extract the URL of the latest invoice PDF file from the webpage.

    Args:
        driver (WebDriver): The Selenium WebDriver instance.

    Returns:
        str: The URL of the PDF file if found, otherwise None.
    """
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

        # Extract PDF url
        pdf_url_start = onclick_attr.find("'") + 1
        pdf_url_end = onclick_attr.rfind("'")
        pdf_url = onclick_attr[pdf_url_start:pdf_url_end]

        return pdf_url

    return None
    
def save_invoice_pdf(epm_contract_code, pdf_url):
    """
    Download and save the invoice PDF file for the given contract.

    Args:
        epm_contract_code (str): The contract code used to name the PDF file.
        pdf_url (str): The URL of the PDF file to be downloaded.
    """
    response = requests.get(pdf_url)

    if response.status_code == 200:
        if not os.path.exists(INVOICE_DOWNLOAD_PATH):
                os.makedirs(INVOICE_DOWNLOAD_PATH)
                
        save_path = os.path.join(INVOICE_DOWNLOAD_PATH, f"factura_{epm_contract_code}.pdf")
        with open(save_path, "wb") as f:
            f.write(response.content)
        print(f"Archivo PDF guardado en: {save_path}")
    else:
        print(f"Error al descargar el PDF: {response.status_code}")
        
def download_invoice(driver, epm_contract_code):
    """
    Perform the entire process of searching, extracting, and downloading an invoice PDF.

    Args:
        driver (WebDriver): The Selenium WebDriver instance.
        epm_contract_code (str): The contract code used to search for invoices.
    """
    search_contract_invoices(driver, epm_contract_code)
    time.sleep(1) 
    pdf_url = extract_invoice_pdf_url(driver)
    time.sleep(1)
    if pdf_url:
        save_invoice_pdf(epm_contract_code, pdf_url)