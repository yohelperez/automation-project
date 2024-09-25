import subprocess
import time
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from common.constants import CHROME_EXECUTABLE, USER_DATA_DIR, REMOTE_DEBUGGING_PORT

def start_remote_chrome():
    """
    Start Chrome with remote debugging enabled.
    """
    command = [CHROME_EXECUTABLE, f"--remote-debugging-port={REMOTE_DEBUGGING_PORT}", f"--user-data-dir={USER_DATA_DIR}"]
    subprocess.Popen(command)
    time.sleep(3) 

def initialize_driver():
    """
    Initialize Selenium WebDriver to connect to an existing remote Chrome session.
    
    Returns:
        driver (WebDriver): Selenium WebDriver instance connected to the remote Chrome session.
    """
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", f"127.0.0.1:{REMOTE_DEBUGGING_PORT}")  # Connect to remote debugging session
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")  # Disable automation flags
    driver = webdriver.Chrome(options=chrome_options)
    
    return driver

def close_new_window(driver):
    """
    Detect and close any new window that opens due to the debugging process.
    
    Args:
        driver (WebDriver): The Selenium WebDriver instance.
    """
    windows_before = set(driver.window_handles)
    start_remote_chrome()  # Start Chrome in remote debugging mode
    windows_after = set(driver.window_handles)

    # Identify and close the newly opened window
    new_window = windows_after - windows_before
    if new_window:
        new_window_handle = new_window.pop()  # Get the handle of the new window
        driver.switch_to.window(new_window_handle)
        driver.close()

def start_browser():
    """
    Start the browser by initializing the WebDriver and managing new windows.
    
    Returns:
        driver (WebDriver): The initialized Selenium WebDriver instance.
    """
    driver = initialize_driver()
    close_new_window(driver)
    
    return driver
