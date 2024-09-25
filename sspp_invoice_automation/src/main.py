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

def main():
    """Main function to start sspp invoice register and download."""
    
    try:
        contract_code = "AD4878"
        epm_contract_code = "9524567"
        property_address = "CL 43 86 A 41 IN 301"
        
        # Browser initialization
        driver = start_browser()
        switch_to_window_with_url(driver, EPM_URL, EPM_SESSION_URL)
        
        # User login
        if is_user_logged_in(driver) == False:
            print("user not logged in, loging")
            login(driver)
        
        # Register invoice
        register_invoice(driver, epm_contract_code, property_address)
        
        # Download invoice
        time.sleep(2) 
        download_invoice(driver, epm_contract_code)
        
        driver.quit()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()

