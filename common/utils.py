import random
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

def perform_action_with_delay(action, *args, **kwargs):
    """Perform the given action with a random delay."""
    action(*args, **kwargs)
    time.sleep(random.uniform(1, 3)) 

def get_shadow_hosts_by_tag_name(driver, tag_name):
    shadow_hosts = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, tag_name))
    )
    
    return shadow_hosts
    
def click_button_in_shadow_at_index(driver, shadow_host_index):
    try:
        shadow_hosts = get_shadow_hosts_by_tag_name(driver, "epm-button")
        shadow_root = driver.execute_script('return arguments[0].shadowRoot', shadow_hosts[shadow_host_index])
        button = shadow_root.find_element(By.CSS_SELECTOR, 'button#button')
        driver.execute_script("arguments[0].click();", button)
    except Exception as e:
        print(f"Error: {e}")

def enter_text_in_shadow_input_at_index(driver, shadow_host_index, text):
    try:
        shadow_hosts = get_shadow_hosts_by_tag_name(driver, "epm-input")
        
        shadow_root = driver.execute_script('return arguments[0].shadowRoot', shadow_hosts[shadow_host_index])
        input_element = shadow_root.find_element(By.CSS_SELECTOR, 'input#input')
        input_element.clear()  
        input_element.send_keys(text) 
    except Exception as e:
        print(f"Error: {e}")