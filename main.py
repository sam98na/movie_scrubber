import pprint
import time

import yaml
from alamo_parser import main_alamo_scraper, get_current_day_data, mold_to_amc_format, get_seven_days_of_alamo_data
from amc_parser import get_unique_names, main_amc_scraper, get_seven_days_of_amc_data
from utils import export_as_json

config = yaml.safe_load(open("config.yaml", "r"))

def overall_scraper():
    start_time = time.time()
    to_return = {}

    # Alamo Code Block
    alamo_locations = {"alamo_sf_link": ["Mountain View", "Valley Fair", "San Francisco"]}
    for config_link in alamo_locations:
        for location in alamo_locations[config_link]:
            indiv_alamo_start_time = time.time()
            alamo_data = main_alamo_scraper(config[config_link], location)
            formatted_data = mold_to_amc_format(alamo_data)
            current_week_data = get_seven_days_of_alamo_data(formatted_data)
            unique_movies = list(get_unique_names(current_week_data))

            print(f"Alamo \"{location}\" parsed.")
            to_return[f"Alamo {location}"] = {"data": current_week_data, "unique_movies": unique_movies}

            indiv_alamo_end_time = time.time()
            print(f"Alamo \"{location}\" parsed in {indiv_alamo_end_time - indiv_alamo_start_time} seconds.")
    alamo_end_time = time.time()
    print(f"Alamo scraper completed in {alamo_end_time - start_time} seconds.")

    # # AMC Code Block
    # amc_locations = {"amc_mercado_link": "Mercado",
    #                  "amc_sunval_link": "Sunnyvale",
    #                 "amc_metreon_link": "Metreon",
    #                 "amc_kabuki_link": "Kabuki",
    #                 "amc_baystreet_link": "Bay Street"}
    # for config_link in amc_locations:
    #     indiv_amc_start_time = time.time()
    #     amc_data = get_seven_days_of_amc_data(config[config_link])
    #     unique_movies = get_unique_names(amc_data)

    #     print(f"AMC \"{amc_locations[config_link]}\" parsed.")
    #     to_return[f"AMC {amc_locations[config_link]}"] = {"data": amc_data, "unique_movies": unique_movies}
        
    #     indiv_amc_end_time = time.time()
    #     print(f"AMC \"{amc_locations[config_link]}\" parsed in {indiv_amc_end_time - indiv_amc_start_time} seconds.")
    # amc_end_time = time.time()
    # print(f"AMC scraper completed in {amc_end_time - alamo_end_time} seconds.")

    end_time = time.time()
    print(f"Overall scraper completed in {end_time - start_time} seconds.")
    return to_return

if __name__ == "__main__":
    import json
    output = overall_scraper()
    with open('overall_scraper.json', 'w') as file:
        json.dump(output, file)