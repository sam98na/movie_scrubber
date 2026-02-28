from selenium import webdriver
from selenium_stealth import stealth

def get_text_from_element(element):
    text = element.text
    if not text:
        text = element.get_attribute("innerText")
    if not text:
        text = element.get_attribute("textContent")
    return text

def initialize_webdriver():
    """
        Initializes a headless Chrome WebDriver.
        Returns: 
            webdriver.Chrome: An instance of the Chrome WebDriver.
    """
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("window-size=1920,1080")
    
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(2)

    return driver