import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import time
from common.webdriver_setup import start_browser
from common.browser_manager import switch_to_window_with_url
from sspp_login import is_user_logged_in, login
from sspp_invoice_download import download_invoice
from sspp_invoice_constants import EPM_URL, EPM_SESSION_URL
from sspp_invoice_register import register_invoice
import pandas as pd
from common.google_services import get_gspread_client, upload_pdf_to_drive
from common.constants import FACTURAS_EPM_FOLDER_ID, DOWNLOAD_PATH
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

def main():
    """Main function to start sspp invoice register and download."""
    
    try:
        """
        # client = get_gspread_client()
        epm_contract = "9524567"
        file_name = f"factura_{epm_contract}"
        file_path = f"{DOWNLOAD_PATH}/{file_name}.pdf"
        upload_pdf_to_drive(file_path, FACTURAS_EPM_FOLDER_ID)
        spreadsheet = client.open("contratos_epm").worksheet("Hoja 1")

        # Read data and convert to dataframe
        data = spreadsheet.get_all_records()
        df = pd.DataFrame(data)

        for index, row in df.iterrows():
            contract_code = row['Contrato EPM']
            property_address = row['Direccion']
            
            # Hacer algo con los valores extraídos
            print(f"Contrato EPM: {contract_code}, Dirección: {property_address}")"""
        
        # Browser initialization
        driver = start_browser()
        switch_to_window_with_url(driver, EPM_URL, EPM_SESSION_URL)       
        
        # Get Google spreadsheets client and spreadsheet
        client = get_gspread_client()
        spreadsheet = client.open("contratos_epm").worksheet("Hoja 1")
        
        # Read data and convert to dataframe
        data = spreadsheet.get_all_records()
        df = pd.DataFrame(data)

        for index, row in df.iterrows():
            # User login
            if is_user_logged_in(driver) == False:
                print("user not logged in, loging")
                login(driver)
            
            epm_contract_code = row['Contrato EPM']
            property_address = row['Direccion']
            
            # Hacer algo con los valores extraídos
            print(f"Contrato EPM: {epm_contract_code}, Dirección: {property_address}")    
            
            
            # Register invoice
            register_invoice(driver, epm_contract_code, property_address)
            
            # Extract invoice
            # to do:
            
            # Upload file to drive
            file_name = f"factura_{epm_contract_code}"
            file_path = f"{DOWNLOAD_PATH}/{file_name}.pdf"
            # upload_pdf_to_drive(file_path, FACTURAS_EPM_FOLDER_ID)
            
            
            
            
            
        
        
        """# User login
        if is_user_logged_in(driver) == False:
            print("user not logged in, loging")
            login(driver)
        
        # Register invoice
        register_invoice(driver, epm_contract_code, property_address)
        
        # Download invoice
        time.sleep(2) 
        download_invoice(driver, epm_contract_code)
        
        driver.quit() """
        
        
        #https://aplicaciones.epm.com.co/facturaweb/#/
        #//*[@id="epm-uuid-4fb53283-e037-4317-a2ed-d89045438904"] yohel button
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()

