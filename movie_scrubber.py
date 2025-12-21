from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from collections import defaultdict
from time import sleep


options = webdriver.ChromeOptions()
# user_agent = UserAgent().random
# options.add_argument(f"user-agent={user_agent}")
# options.add_argument("start-maximized")
# options.add_argument("--headless")
# options.add_experimental_option("excludeSwitches", ["enable-automation"])
# options.add_experimental_option('useAutomationExtension', False)


driver = webdriver.Chrome(options=options)


list_of_non_movies = ["See a Movie", "Find a Theatre", "", "Assistive Moviegoing", "Watch Video", "Discover More", 
                      "Movies", "Theatres", "Movie Merchandise"]
list_of_non_movies = [i.upper() for i in list_of_non_movies]

amc_dict = defaultdict(int)
alamo_dict = defaultdict(int)

def non_movie_stripper(defdict, non_movies):
    for i in non_movies:
        try:
            del defdict[i]
        except Exception:
            pass   

def movies_fetcher(web_driver: webdriver.Chrome, address, driver_selector, driver_selector_string, count_dict, alamo):
    web_driver.get(address)
    web_driver.implicitly_wait(20)
    sleep(5)
    if alamo:
        button_text = "Mountain View"
        try:
            button = web_driver.find_element(By.XPATH, f"//button[contains(text(),'{button_text}')]")
            web_driver.implicitly_wait(20)
            button.click()
            sleep(5)
            print(f"Button with text '{button_text}' clicked successfully (exact match).")
        except Exception as e:
            print(repr(e))
            print(f"Button with text '{button_text}' not found or not clickable")
    fetched_movie_names = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((driver_selector, driver_selector_string)))
    movie_names = [i.text.upper() for i in fetched_movie_names]
    print(f"Waited elements: {movie_names}")
    web_driver.implicitly_wait(20)
    for i in movie_names:
        count_dict[i] += 1
 
# create webdriver object
stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        webdriver=False,
        fix_hairline=True)

sunnyvale_amc_link = "https://www.amctheatres.com/movie-theatres/san-francisco/amc-dine-in-sunnyvale-12/showtimes"
mercado_amc_link = "https://www.amctheatres.com/movie-theatres/san-francisco/amc-mercado-20/showtimes"
alamo_link = "https://www.drafthouse.com/sf?showCalendar=true"


 
#amc sunnyvale
movies_fetcher(driver, sunnyvale_amc_link,
               By.CSS_SELECTOR, "a[href*='/movies']:not([href*='showtime'])", amc_dict, False)

#amc mercado
# movies_fetcher(driver, mercado_amc_link,
#                By.CSS_SELECTOR, "a[href*='/movies']:not([href*='showtime'])", amc_dict, False)

# #alamo
movies_fetcher(driver, alamo_link,
               By.CLASS_NAME, "calendar_showlink", alamo_dict, True)

#alamo css selector version
# movies_fetcher(driver, alamo_link,
#                By.CSS_SELECTOR, "a[href*='/show/']", alamo_dict, True)

# #regal
# movies_fetcher(driver, "https://www.regmovies.com/movies",
#                By.XPATH, "//figcaption[descendant::div]", counted)

non_movie_stripper(amc_dict, list_of_non_movies)
non_movie_stripper(alamo_dict, list_of_non_movies)
print(amc_dict)
print(alamo_dict)

combined = defaultdict(int)
amc_movies, alamo_movies = set(list(amc_dict.keys())), set(list(alamo_dict.keys()))
for i in amc_dict.keys():
    combined[i] += amc_dict[i]
for i in alamo_dict.keys():
    combined[i] += alamo_dict[i]

sorted_all_movies = sorted(combined.items(), key = lambda x: x[1], reverse=True)

print("### MOVIES ###")
print("Popular Movies")
for i in sorted_all_movies:
    if i[1] >= 2:
        print(f"-- {i[0]} || {'::AMC::' if i[0] in amc_movies else ''} {'::ALAMO::' if i[0] in alamo_movies else ''}")
print("\n\n")

print("Less Popular Movies")
for i in sorted_all_movies:
    if i[1] < 2 and (i[0] in amc_movies and i[0] in alamo_movies) or (i[0] in amc_movies and i[0] not in alamo_movies):
        print(f"-- {i[0]} || {'::AMC::' if i[0] in amc_movies else ''} {'::ALAMO::' if i[0] in alamo_movies else ''}")
print("\n\n")

print("Alamo Exclusive Movies")
for i in sorted_all_movies:
    if i[1] < 2 and i[0] not in amc_movies and i[0] in alamo_movies:
        print(f"-- {i[0]}")



driver.close()

 