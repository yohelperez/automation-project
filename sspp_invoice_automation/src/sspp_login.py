from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from sspp_invoice_constants import EPM_HOME_URL, USER_EMAIL, USER_PASSWORD

def is_user_logged_in(driver): 
    """
    Check if the user is logged in.

    Args:
        driver (WebDriver): The Selenium WebDriver instance.

    Returns:
        bool: True if the user is logged in, False otherwise.
    """
    try:
        driver.find_element(By.XPATH, '//*[@id="ctl00_lblNombre"]')
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
        driver.get(EPM_HOME_URL)
        email_field = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="ctl00_cphPrincipal_txtCorreo"]'))
        )
        email_field.send_keys(USER_EMAIL)

        password_field = driver.find_element(By.XPATH, '//*[@id="ctl00_cphPrincipal_txtClave"]')
        password_field.send_keys(USER_PASSWORD)

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