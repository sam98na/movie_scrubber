from utils import get_text_from_element, initialize_webdriver

from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from collections import defaultdict
from time import sleep
import yaml
import pprint

config = yaml.safe_load(open("config.yaml", "r"))

def main_amc_scraper(amc_link, date):
    print("Starting AMC Scraper")
    driver = initialize_webdriver()

    driver.get(amc_link + date)
    print("-- AMC page loaded --")
    sleep(5)

    fetched_showtime_objects = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, "//*[@aria-label[starts-with(., 'Depart')]]")))
    print("-- Processed all available Showtime elements --")
    overall_data = {}
    for row in fetched_showtime_objects:
        all_as = row.find_elements(By.TAG_NAME, "a")
        for a in all_as:
            print(get_text_from_element(a))

    driver.quit()
    return overall_data

if __name__ == "__main__":
    amc_data = main_amc_scraper(config["amc_sunval_link"], "2026-02-23")
    pprint.pprint(amc_data)