from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta

from utils import convert_date_to_uniform, get_text_from_element, initialize_webdriver, get_current_datetime_pst

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
    overall_data, days_processed = process_calendar_row(fetched_calendar_rows, overall_data)

    if days_processed < 7:
        try:
            next_month_dt = date.today() + timedelta(weeks=3)
            next_month = next_month_dt.strftime("%B %Y")
            button = driver.find_element(By.XPATH, f"//button[contains(text(),'{next_month}')]")
            button.click()
            sleep(5)
            print(f"-- Insubstantial calendar days parsed, {next_month}' button clicked successfully (exact match). --")

            fetched_calendar_rows = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "calendar_row")))
            overall_data, days_processed = process_calendar_row(fetched_calendar_rows, overall_data)
        except Exception as e:
            print(repr(e))
            print(f"-- '{next_month}' button not found or not clickable --")

    driver.quit()
    return overall_data

def process_calendar_row(calendar_row, overall_data):
    days_processed = 0
    for row in calendar_row:
        calendar_day = row.find_elements(By.CSS_SELECTOR, "td.calendar_day:not(.calendar_day--empty)")
        print(f"-- Available calendar days processed: {len(calendar_day)} --")
        days_processed += len(calendar_day)
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
    return overall_data, days_processed

def get_current_day_data(overall_data):
    current_day = get_current_datetime_pst().strftime("%Y-%m-%d")
    return overall_data.get(current_day, {})

def get_unique_names(current_data):
    return set(current_data.keys())

def mold_to_amc_format(current_data):
    molded_data = {}
    for date, movie_items in current_data.items():
        molded_data[date] = {}
        for movie_name, showtimes in movie_items.items():
            molded_data[date][movie_name.upper().strip()] = {
                "formats": [
                    {
                        "format_name": "Alamo Standard",
                        "attributes": [],
                        "showtimes": showtimes
                    }
                ]
            }
    return molded_data

def get_seven_days_of_alamo_data(overall_data, start_date=None):
    """Return a `{YYYY-MM-DD: day_data}` slice covering 7 consecutive days
    starting at `start_date` (defaults to today). Missing days fall back to an
    empty dict so downstream code can rely on every key being present."""
    if start_date is None:
        start_dt = get_current_datetime_pst() 
    else:
        start_dt = datetime.strptime(start_date, "%Y-%m-%d")
    seven_days_data = {}
    for i in range(7):
        day_key = (start_dt + timedelta(days=i)).strftime("%Y-%m-%d")
        seven_days_data[day_key] = overall_data.get(day_key, {})
    return seven_days_data

def get_unique_names(current_data):
    to_return = set()
    for date, movie_items in current_data.items():
        for movie_name in movie_items.keys():
            to_return.add(movie_name)
    return to_return

if __name__ == "__main__":
    alamo_data = main_alamo_scraper(config["alamo_sf_link"], "Mountain View")
    molded_data = mold_to_amc_format(alamo_data)
    pprint.pprint(molded_data)