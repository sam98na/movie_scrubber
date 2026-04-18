import datetime

from utils import convert_date_to_uniform, get_text_from_element, initialize_webdriver

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

def main_alamo_scraper(alamo_link, button_text):
    print("-- Starting Alamo Scraper --")
    driver = initialize_webdriver()

    driver.get(alamo_link)
    print("-- Alamo page loaded --")
    sleep(5)
    if button_text:
        try:
            button = driver.find_element(By.XPATH, f"//button[contains(text(),'{button_text}')]")
            button.click()
            sleep(5)
            print(f"-- {button_text}' button clicked successfully (exact match). --")
        except Exception as e:
            print(repr(e))
            print(f"-- '{button_text}' button not found or not clickable --")
    fetched_calendar_rows = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "calendar_row")))
    print("-- Processed all available calendar rows --")
    overall_data = {}
    for row in fetched_calendar_rows:
        calendar_day = row.find_elements(By.CSS_SELECTOR, "td.calendar_day:not(.calendar_day--empty)")
        print(f"-- Available calendar days processed: {len(calendar_day)} --")
        for calendar_day in calendar_day:
            dateElement = calendar_day.find_element(By.CSS_SELECTOR, "span.calendar_dayDate:not(.bodyText-strong)")
            dateText = convert_date_to_uniform(get_text_from_element(dateElement))
            overall_data[dateText] = {}

            movieElements = calendar_day.find_elements(By.TAG_NAME, "li")
            for movies in movieElements:
                movieName = movies.find_element(By.CLASS_NAME, "calendar_showlink")
                movieNameText = get_text_from_element(movieName).strip()
                overall_data[dateText][movieNameText] = []
                showtimes = movies.find_elements(By.CLASS_NAME, "calendar_showtimes")[0].find_elements(By.TAG_NAME, "a")
                for showtime in showtimes:
                    showtimeText = get_text_from_element(showtime)
                    overall_data[dateText][movieNameText].append(showtimeText)

    driver.quit()
    return overall_data

def get_current_day_data(overall_data):
    current_day = datetime.datetime.now().strftime("%Y-%m-%d")
    return overall_data.get(current_day, {})

def get_unique_names(current_data):
    return set(current_data.keys())

def mold_to_amc_format(current_data):
    molded_data = {}
    for movie_name, showtimes in current_data.items():
        molded_data[movie_name.upper().strip()] = {
            "formats": [
                {
                    "format_name": "Alamo Standard",
                    "attributes": [],
                    "showtimes": showtimes
                }
            ]
        }
    return molded_data

if __name__ == "__main__":
    alamo_data = main_alamo_scraper(config["alamo_sf_link"], "Mountain View")
    molded_data = mold_to_amc_format(alamo_data)
    pprint.pprint(molded_data)