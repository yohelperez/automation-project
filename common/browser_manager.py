def find_window_by_url(driver, target_url):
    """
    Search through all open browser windows for a specific URL and return the window handle.

    Args:
        driver (webdriver.Chrome): The Selenium WebDriver instance controlling the browser.
        target_url (str): The URL to search for among the open browser windows.

    Returns:
        str: The handle of the window that matches the target URL, or None if no match is found.
    """
    for handle in driver.window_handles:
        driver.switch_to.window(handle)
        if target_url in driver.current_url:
            return handle
    return None

def switch_to_window_with_url(driver, target_url, fallback_url):
    """
    Switch to a browser window that contains the target URL. 
    If no window is found, open a new window with the fallback URL.

    Args:
        driver (webdriver.Chrome): The Selenium WebDriver instance controlling the browser.
        target_url (str): The URL to search for among the open browser windows.
        fallback_url (str): The URL to load in a new browser window if the target URL is not found.

    Returns:
        None
    """
    found_window = find_window_by_url(driver, target_url)

    if found_window:
        driver.switch_to.window(found_window)
    else:
        try:
            driver.get(fallback_url)
        except Exception as e:
            print(f"Error al intentar abrir la URL: {fallback_url}. Detalle del error: {e}")

