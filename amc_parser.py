import os
import re
import sys

from utils import get_text_from_element, initialize_webdriver, clean_amc_format, get_current_datetime_pst

from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from collections import defaultdict
from time import sleep
from datetime import datetime, timedelta
import yaml
import pprint

config = yaml.safe_load(open("config.yaml", "r"))

def main_amc_scraper(amc_link, date=get_current_datetime_pst().strftime("%Y-%m-%d")):
    print("-- Starting AMC Scraper --")
    driver = initialize_webdriver()

    driver.get(amc_link + date)
    print("-- Page loaded --")
    sleep(2)

    fetched_showtime_objects = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, "//section[starts-with(@aria-label, 'Showtimes for')]")))
    print("-- Processed all available Showtime elements --")
    overall_data = {}
    for row in fetched_showtime_objects:
        current_object = {}
        movie_name = row.find_elements(By.XPATH, ".//h1//a[starts-with(@href, '/movies/')]")
        movie_name = get_text_from_element(movie_name[0])
        movie_name = movie_name.upper().strip()

        formats = row.find_elements(By.XPATH, "./div[starts-with(@aria-label, 'Showtimes at')]/ul[contains(@aria-label, 'Showtimes')]/li")
        for li_s in formats:
            format_object = {}
            format_name = clean_amc_format(li_s.get_attribute("aria-label"))
            format_object["format_name"] = format_name

            relevant_attributes = []
            attributes = li_s.find_elements(By.XPATH, ".//ul[contains(@id, 'attributes')]/li")
            for attribute in attributes:
                curr_attribute_text = get_text_from_element(attribute)
                if any(keyword in curr_attribute_text for keyword in ["Excluded", "Subtitle"]):
                    relevant_attributes.append(curr_attribute_text)
            format_object["attributes"] = relevant_attributes

            showtimes = []
            showtime_containers = li_s.find_elements(By.XPATH, ".//ul[@aria-label = 'Showtime Group Results']/li")
            for showtime_container in showtime_containers:
                showtime = get_text_from_element(showtime_container.find_element(By.XPATH, ".//a[contains(@href, '/showtimes/')]"))
                showtime = re.search("\d{1,2}:\d{2}[ap]m", showtime)
                if showtime:
                    showtime = showtime.group(0)
                    showtimes.append(showtime)
            format_object["showtimes"] = showtimes
            if "formats" not in current_object:
                current_object["formats"] = []
            current_object["formats"].append(format_object)
        overall_data[movie_name] = current_object

    driver.quit()
    return overall_data

def get_seven_days_of_amc_data(amc_link, start_date=None):
    """Scrape 7 consecutive days of AMC data starting at `start_date`
    (defaults to today), returning `{YYYY-MM-DD: day_data}`."""
    if start_date is None:
        start_dt = get_current_datetime_pst()
    else:
        start_dt = datetime.strptime(start_date, "%Y-%m-%d")
    overall_data = {}
    for i in range(7):
        day_key = (start_dt + timedelta(days=i)).strftime("%Y-%m-%d")
        print(f"Current day: {day_key}")
        overall_data[day_key] = main_amc_scraper(amc_link, day_key)
    return overall_data

def get_unique_names(overall_data):
    to_return = set()
    for date, movie_items in overall_data.items():
        for movie_name in movie_items.keys():
            to_return.add(movie_name)
    return to_return

if __name__ == "__main__":
    amc_data = main_amc_scraper(config["amc_sunval_link"])
    pprint.pprint(amc_data)