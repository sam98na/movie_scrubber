import pprint

import yaml
from alamo_parser import main_alamo_scraper, get_current_day_data, mold_to_amc_format
from amc_parser import get_unique_names, main_amc_scraper
from utils import export_as_json

config = yaml.safe_load(open("config.yaml", "r"))

def overall_scraper():
    mt_alamo_data = main_alamo_scraper(config["alamo_sf_link"], "Mountain View")
    current_day_mt_data = get_current_day_data(mt_alamo_data)
    export_as_json(current_day_mt_data, "saved_jsons/alamo_mt_data.json")
    mt_unique_movies = get_unique_names(current_day_mt_data)

    vf_alamo_data = main_alamo_scraper(config["alamo_sf_link"], "Valley Fair")
    export_as_json(vf_alamo_data, "saved_jsons/alamo_vf_data.json")
    current_day_vf_data = get_current_day_data(vf_alamo_data)
    vf_unique_movies = get_unique_names(current_day_vf_data)

    # sf_alamo_data = main_alamo_scraper(config["alamo_sf_link"], "San Francisco")
    # current_day_sf_data = get_current_day_data(sf_alamo_data)
    # sf_unique_movies = get_unique_names(current_day_sf_data)

    sunnyvale_amc_data = main_amc_scraper(config["amc_sunval_link"])
    export_as_json(sunnyvale_amc_data, "saved_jsons/amc_sunnyvale_data.json")
    sunnyvale_unique_movies = get_unique_names(sunnyvale_amc_data)

    mercado_amc_data = main_amc_scraper(config["amc_mercado_link"])
    export_as_json(mercado_amc_data, "saved_jsons/amc_mercado_data.json")
    mercado_unique_movies = get_unique_names(mercado_amc_data)

    print(mt_unique_movies)
    print(vf_unique_movies)
    print(sunnyvale_unique_movies)
    print(mercado_unique_movies)

    common_movies = set.intersection(mt_unique_movies, vf_unique_movies, sunnyvale_unique_movies, mercado_unique_movies)
    print("Movies playing at both AMC and Alamo today:")
    for movie in common_movies:
        print(f"-- {movie}")
    print("\n\n")

    print("Special movies playing at AMC Sunnyvale today:")
    for movie in sunnyvale_unique_movies:
        if movie not in common_movies:
            print(f"-- {movie} (AMC Sunnyvale)")
    print("\n\n")

    print("Special movies playing at AMC Mercado today:")
    for movie in mercado_unique_movies:
        if movie not in common_movies:
            print(f"-- {movie} (AMC Mercado)")
    print("\n\n")

    print("Special movies playing at Alamo (Mountain View) today:")
    for movie in mt_unique_movies:
        if movie not in common_movies:
            print(f"-- {movie} (Alamo Mountain View)")
    print("\n\n")

    print("Special movies playing at Alamo (Valley Fair) today:")
    for movie in vf_unique_movies:
        if movie not in common_movies:
            print(f"-- {movie} (Alamo Valley Fair)")
    print("\n\n")

    molded_mt_data = mold_to_amc_format(current_day_mt_data)
    molded_vf_data = mold_to_amc_format(current_day_vf_data)
    toReturn = {"Alamo Mountain View": molded_mt_data, 
                "Alamo Valley Fair": molded_vf_data,
                "AMC Sunnyvale": sunnyvale_amc_data,
                "AMC Mercado": mercado_amc_data}
    return toReturn

def loaded_scraper():
    with open("saved_jsons/alamo_mt_data.json", "r") as f:
        mt_data = yaml.safe_load(f)
    with open("saved_jsons/alamo_vf_data.json", "r") as f:
        vf_data = yaml.safe_load(f)
    with open("saved_jsons/amc_sunnyvale_data.json", "r") as f:
        sunnyvale_data = yaml.safe_load(f)
    with open("saved_jsons/amc_mercado_data.json", "r") as f:
        mercado_data = yaml.safe_load(f)

    mt_unique_movies = get_unique_names(mt_data)
    vf_unique_movies = get_unique_names(vf_data)
    sunnyvale_unique_movies = get_unique_names(sunnyvale_data)
    mercado_unique_movies = get_unique_names(mercado_data)

    pprint.pprint(mold_to_amc_format(mt_data))
    print("\n\n")
    pprint.pprint(sunnyvale_data)

if __name__ == "__main__":
    overall_scraper()