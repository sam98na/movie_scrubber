import os
import sys
import yaml
import requests
from rapidfuzz import fuzz, process

from utils import year_from_string

config = yaml.safe_load(open("config.yaml", "r"))

# tmdb_api_key = os.environ.get("TMDB_API_KEY")
tmdb_movie_search_link = config["tmdb_movie_search_link"]
tmdb_movie_metadata_link = config["tmdb_movie_metadata_link"]

def movie_search(movie_name):
    url = tmdb_movie_search_link.format(movie_name=movie_name.replace(" ", "%20"))
    headers = {
        'Authorization': f'Bearer {tmdb_api_key}',
        'accept': 'application/json'
    }
    response = requests.get(url, headers=headers)
    return response.json()["results"]

def get_movie_metadata(movie_id):
    url = tmdb_movie_metadata_link.format(movie_id=movie_id)
    headers = {
        'Authorization': f'Bearer {tmdb_api_key}',
        'accept': 'application/json'
    }
    response = requests.get(url, headers=headers).json()
    to_return = {"id": response["id"], 
                "runtime": response["runtime"], 
                "release_date": year_from_string(response["release_date"]),
                "overview": response["overview"]}
    return to_return

def get_most_similar_movie(movie_name, response_json):
    for i in response_json:
        if fuzz.ratio(movie_name, i["title"]) > 80:
            return i
    return None

def indiv_movie_search(movie_name):
    """Return TMDB metadata for the closest match to `movie_name`, or None if
    no sufficiently similar title is returned by the search endpoint."""
    search_results = movie_search(movie_name)
    print(search_results)
    most_similar_movie = get_most_similar_movie(movie_name, search_results)
    print(most_similar_movie)
    if most_similar_movie is None:
        return None
    return get_movie_metadata(most_similar_movie["id"])

def overall_movie_search(list_of_movie_names):
    """Best-effort TMDB enrichment for a batch of titles.

    Titles that can't be matched (or whose TMDB request fails) are simply
    omitted from the result so a single bad title doesn't take down the batch.
    """
    to_return = {}
    for movie_name in list_of_movie_names:
        try:
            movie_metadata = indiv_movie_search(movie_name)
        except Exception as e:
            print(f"-- TMDB lookup failed for {movie_name!r}: {e!r} --")
            continue
        if movie_metadata is not None:
            to_return[movie_name] = movie_metadata
    return to_return

if __name__ == "__main__":
    # import json
    # with open('overall_scraper.json', 'r') as file:
    #     movie_data = json.load(file)
    # combined_movies = set()
    # for key in movie_data:
    #     print(movie_data[key]["unique_movies"])
    #     print("\n")
    #     combined_movies.update(set(movie_data[key]["unique_movies"]))
    # metadata = overall_movie_search([i.replace(" ", "%20") for i in list(combined_movies)])
    # with open('tmdb_metadata.json', 'w') as file:
    #     json.dump(metadata, file)
    returna = overall_movie_search(["The Drama"])
    print(returna["The Drama"])