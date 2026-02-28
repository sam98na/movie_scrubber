import yaml
from alamo_parser import main_alamo_scraper

config = yaml.safe_load(open("config.yaml", "r"))

if __name__ == "__main__":
    mt_alamo_data = main_alamo_scraper(config["alamo_sf_link"], "Mountain View")
    vf_alamo_data = main_alamo_scraper(config["alamo_sf_link"], "Valley Fair")
    sf_alamo_data = main_alamo_scraper(config["alamo_sf_link"], "San Francisco")