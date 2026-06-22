import pprint
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

import yaml
from alamo_parser import main_alamo_scraper, get_current_day_data, mold_to_amc_format, get_seven_days_of_alamo_data
from amc_parser import get_unique_names, main_amc_scraper, get_seven_days_of_amc_data
from utils import export_as_json, movie_similarity_check

config = yaml.safe_load(open("config.yaml", "r"))

def alamo_scraper(config_link, location):
    try:
        indiv_alamo_start_time = time.time()
        alamo_data = main_alamo_scraper(config[config_link], location)
        formatted_data = mold_to_amc_format(alamo_data)
        current_week_data = get_seven_days_of_alamo_data(formatted_data)
        unique_movies = list(get_unique_names(current_week_data))
        indiv_alamo_end_time = time.time()
        print(f"Alamo \"{location}\" parsed in {indiv_alamo_end_time - indiv_alamo_start_time} seconds.")

        return f"Alamo {location}", {"data": current_week_data, "unique_movies": unique_movies}
    except Exception as e:
        print(f"Parsing for Alamo {location} failed. Reason: {e}")
        return None
    
def amc_scraper(config_link, amc_locations):
    try:
        indiv_amc_start_time = time.time()
        amc_data = get_seven_days_of_amc_data(config[config_link])
        unique_movies = get_unique_names(amc_data)
        indiv_amc_end_time = time.time()
        print(f"AMC \"{amc_locations[config_link]}\" parsed in {indiv_amc_end_time - indiv_amc_start_time} seconds.")

        return f"AMC {amc_locations[config_link]}", {"data": amc_data, "unique_movies": unique_movies}
    except Exception as e:
        print(f"Parsing for AMC {amc_locations[config_link]} failed. Reason: {e}")
        return None

def overall_scraper():
    start_time = time.time()
    to_return = {}
    with ThreadPoolExecutor() as executor:
        # Alamo Code Block
        alamo_config_link = "alamo_sf_link"
        alamo_locations = ["Mountain View", "Valley Fair", "San Francisco"]
        futures = {executor.submit(alamo_scraper, alamo_config_link, location): f"Alamo {location}" for location in alamo_locations}

        # AMC Code Block
        amc_locations = {"amc_mercado_link": "Mercado",
                        "amc_sunval_link": "Sunnyvale",
                        "amc_metreon_link": "Metreon",
                        "amc_kabuki_link": "Kabuki",
                        "amc_baystreet_link": "Bay Street"}
        futures = {**futures, **{executor.submit(amc_scraper, key, amc_locations): f"AMC {value}" for key, value in amc_locations.items()}}

    for future in as_completed(futures):
        label = futures[future]
        try:
            key, data = future.result()
            to_return[key] = data
        except Exception as e:
            print(f"Failed for {label}: {e}")        

    end_time = time.time()
    print(f"Overall scraper completed in {end_time - start_time} seconds.")
    return to_return

def coalescer(scraped_data):
    to_return = {}
    for movie_theater in scraped_data.keys():
        curr_theater_data = scraped_data[movie_theater]["data"]
        for date in curr_theater_data.keys():
            curr_date_movies = curr_theater_data[date]
            for movie in curr_date_movies.keys():
                if date not in to_return:
                    to_return[date] = {}
                added = False
                for existing_movie_name in to_return[date].keys():
                    if movie_similarity_check(movie, existing_movie_name):
                        to_return[date][existing_movie_name][movie_theater]["formats"] += curr_date_movies[movie]["formats"]
                        added = True
                if not added:
                    to_return[date][movie][movie_theater] = curr_date_movies[movie]
    return to_return
                

if __name__ == "__main__":
    import json
    current_time = time.time()
    output = overall_scraper()
    with open(f'overall_scraped_{current_time}.json', 'w') as file:
        json.dump(output, file)
    coalesced = coalescer(output)
    with open(f'overall_coalesced_{current_time}.json', 'w') as file:
        json.dump(output, file)