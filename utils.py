import re

from selenium import webdriver
from selenium_stealth import stealth
from datetime import datetime

def get_text_from_element(element):
    text = element.text
    if not text:
        text = element.get_attribute("innerText")
    if not text:
        text = element.get_attribute("textContent")
    return text

def convert_date_to_uniform(date_str):
    """
        Converts a date string to a uniform format (YYYY-MM-DD).
        Args:
            date_str (str): The input date string.
        Returns:
            str: The converted date string in uniform format.
    """
    try:
        current_year = datetime.strftime(datetime.now(), "%Y")
        date_obj = datetime.strptime(date_str, "%a, %b %d")
        return current_year + "-" + date_obj.strftime("%m-%d")
    except ValueError:
        print("Error parsing date string:", date_str)
        return date_str  # Return original if parsing fails
    
def clean_amc_format(format_str):
    """
        Cleans the AMC format string by removing unnecessary parts.
        Args:
            format_str (str): The input format string.
        Returns:
            str: The cleaned format string.
    """
    return re.sub("at AMC Showtimes|Showtimes", "", format_str).strip()

def initialize_webdriver(headless=True):
    """
        Initializes a headless Chrome WebDriver.
        Returns: 
            webdriver.Chrome: An instance of the Chrome WebDriver.
    """
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument("--headless")
    options.add_argument("window-size=1920,1080")
    
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(2)

    return driver

if __name__ == "__main__":
    print(convert_date_to_uniform("Mon, Mar 9"))