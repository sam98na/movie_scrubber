import os
import sys
import yaml
import requests
import pprint
import re
from rapidfuzz import fuzz, process

from utils import year_from_string

config = yaml.safe_load(open("config.yaml", "r"))

# tmdb_api_key = os.environ.get("TMDB_API_KEY")
tmdb_api_key = 'eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJjYmU5M2Q2MTNhZDdlMGYyMzM3OGE2ZmU0NGI5OWYxMCIsIm5iZiI6MTc3MDgxMTcwOS45MjYsInN1YiI6IjY5OGM3MTNkZTNjNzQwMTBmZTdiZTZhYyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.BI7NxLXITGTyr-1pbjwHLoWFEWos5_wKToSso4DI8lg'
tmdb_movie_search_link = config["tmdb_movie_search_link"]
tmdb_movie_metadata_link = config["tmdb_movie_metadata_link"]

def movie_search(movie_name):
    formatted_movie_name = movie_name_search_string_formatter(movie_name)
    url = tmdb_movie_search_link.format(movie_name=formatted_movie_name.replace(" ", "%20"))
    print(url)
    headers = {
        'Authorization': f'Bearer {tmdb_api_key}',
        'accept': 'application/json'
    }
    response = requests.get(url, headers=headers)
    return response.json()["results"]

def get_movie_metadata(movie_id):
    url = tmdb_movie_metadata_link.format(movieID=movie_id)
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
    use_string = movie_name_search_string_formatter(movie_name)
    for i in response_json:
        if fuzz.token_set_ratio(use_string.lower(), i["title"].lower()) > 80:
            # print(f"### {use_string} FUZZ ABOVE 80 ###")
            # print(i)
            # print("\n\n")
            return i
        elif fuzz.token_set_ratio(use_string.lower(), i["title"].lower()) > 50:
            # print("### {use_string} FUZZ ABOVE 50 ###")
            # print(i)
            print("\n\n")
    print(f"No value for {use_string} was close enough.")
    print(response_json)
    return None

def movie_name_search_string_formatter(movie_name):
    # REMOVES MOVIE PARTY/4K REMASTER FROM ALAMO
    print(f"\n\nMovie name before: {movie_name}")
    subbed = re.sub("(MOVIE PARTY|4K REMASTER|EARLY ACCESS|EARLY ACCESS EVENT|OPENING NIGHT EVENT|HDR BY BARCO)", "" , movie_name)
    # REMOVES ANYTHING AFTER "(" USUALLY USED IN "(DATE)" IN MOVIE NAMES
    match = re.search(r".*(?=\()" , subbed)
    if match:
        toReturn = match.group().strip()
    else:
        toReturn = subbed.strip()

    print(f"Movie name after: {toReturn}\n\n")
    return toReturn

def indiv_movie_search(movie_name):
    """Return TMDB metadata for the closest match to `movie_name`, or None if
    no sufficiently similar title is returned by the search endpoint."""
    search_results = movie_search(movie_name)
    most_similar_movie = get_most_similar_movie(movie_name, search_results)
    if most_similar_movie is None:
        return None
    return get_movie_metadata(most_similar_movie["id"])

def overall_movie_search(list_of_movie_names):
    """Best-effort TMDB enrichment for a batch of titles.

    Titles that can't be matched (or whose TMDB request fails) are simply
    omitted from the result so a single bad title doesn't take down the batch.
    """
    stripped_reference = {}
    to_return = {}
    for movie_name in list_of_movie_names:
        stripped_movie_name = movie_name_search_string_formatter(movie_name)
        if stripped_movie_name in stripped_reference:
            to_return[movie_name] = stripped_reference[stripped_movie_name]
        else:
            try:
                movie_metadata = indiv_movie_search(movie_name)
            except Exception as e:
                print(f"-- TMDB lookup failed for {movie_name!r}: {e!r} --")
                continue
            if movie_metadata is not None:
                to_return[movie_name] = movie_metadata
                stripped_reference[stripped_movie_name] = movie_metadata
    return to_return

if __name__ == "__main__":
    import json
    with open('overall_scraped.json', 'r') as file:
        movie_data = json.load(file)
    combined_movies = set()
    for key in movie_data:
        combined_movies.update(set(movie_data[key]["unique_movies"]))
    print("Combined unique movies")
    print(combined_movies)
    metadata = overall_movie_search(list(combined_movies))
    
    with open('tmdb_metadata.json', 'w') as file:
        json.dump(metadata, file)
    # print(fuzz.token_set_ratio("MET OPERA: EL ULTIMO SUENO DE FRIDA Y DIEGO ENCORE", "The Metropolitan Opera: El Último Sueño de Frida y Diego"))