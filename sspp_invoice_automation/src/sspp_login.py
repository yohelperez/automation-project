import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from sspp_invoice_constants import EPM_LOGIN_URL, USER_EMAIL, USER_PASSWORD
from common.utils import click_button_in_shadow_at_index

def close_popup(driver):
    WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//epm-header-accessibility'))
    )
    
    try:
        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="continuar"]'))
        ).click()
        
    #to do: close possible session time out button
    except TimeoutException:
        print("Botón 'Continuar' no encontrado. Continuando.")

def is_user_logged_in(driver): 
    """
    Check if the user is logged in.

    Args:
        driver (WebDriver): The Selenium WebDriver instance.

    Returns:
        bool: True if the user is logged in, False otherwise.
    """
    try: 
        close_popup(driver)
        driver.find_element(By.XPATH, '//*[@id="sidenav"]/ul/li[2]/a/img')
        return True
    except NoSuchElementException:
        return False

def login(driver):
    """
    Log in to the website using the user email and password.

    Args:
        driver (WebDriver): The Selenium WebDriver instance.
    """
    try:
        driver.get(EPM_LOGIN_URL)
        close_popup(driver)
        time.sleep(1)
        click_button_in_shadow_at_index(driver, 0)
        time.sleep(1)
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="GoogleExchange"]'))
        ).click()
        
        print("Inicio de sesión completado.")
    except TimeoutException:
        print("Error: El elemento esperado no apareció a tiempo. Verifique el proceso de inicio de sesión.")
        raise
    except Exception as e:
        print(f"Ocurrió un error durante el inicio de sesión: {e}")