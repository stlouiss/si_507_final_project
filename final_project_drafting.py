
import requests
import json
import sqlite3
import google_secrets
import yelp_secrets


states = ['alaska', 'alabama', 'arkansas', 'arizona', 'california', 'colorado', 
'connecticut', 'dc', 'district of columbia', 'delaware', 'florida', 'georgia', 'hawaii',
'iowa', 'idaho', 'illinois', 'indiana', 'kansas', 'kentucky', 'louisiana', 
'massachusetts', 'maryland', 'maine', 'michigan', 'minnesota', 'missouri', 'mississippi',
'montana', 'north carolina', 'north dakota', 'nebraska', 'new hampshire', 'new jersey', 
'new mexico', 'nevada', 'new york', 'ohio', 'oklahoma', 'oregon', 'pennsylvania', 
'rhode island', 'south carolina', 'south dakota', 'tennessee', 'texas', 'utah', 'virginia',
'vermont', 'washington', 'wisconsin', 'west virginia', 'wyoming', 'american samoa', 'guam', 
 'northern mariana islands', 'puerto rico', 'virgin islands']


GOOGLE_CACHE_FILE_NAME = 'google_cache.json'
GOOGLE_CACHE_DICT = {}

YELP_CACHE_FILE_NAME = 'yelp_cache.json'
YELP_CACHE_DICT = {}

conn = sqlite3.connect("harvested_data.sqlite")
cur = conn.cursor()


def fetch_google_data(google_baseurl, search_term):
    """
    Takes a URL and a search term (both strings)
    in order to retrieve a JSON object of 
    Google data for up to 20 results relevant
    to the given search term. Then returns the
    JSON as a Python dictionary.

    Parameters
    ----------
    google_baseurl: str
        The URL forming the base of the API query.

    Returns
    ----------
    google_data: dict
        A Python dictionary rendered from
        JSON, comprising the search results, 
        maximum 50.
    """
    params = {"query": search_term, "key": google_secrets.google_api_key, "language": language, "type": place_type}
    response_data = requests.get(google_baseurl, params=params)
    text_data_response = response_data.text
    google_data = json.loads(text_data_response)
    return google_data


def fetch_yelp_data(yelp_baseurl, search_term):
    """
    Takes a URL and a search term (both strings)
    in order to retrieve a JSON object of 
    Yelp data for up to 50 results relevant
    to the given search term. Then returns the
    JSON as a Python dictionary.

    Parameters
    ----------
    yelp_baseurl: str
        The URL forming the base of the API query.

    Returns
    ----------
    yelp_data: dict
        A Python dictionary rendered from
        JSON, comprising the search results, 
        maximum 50.
    """
    headers = {"Authorization": f"Bearer {yelp_secrets.yelp_api_key}"}
    params = {"categories": category, "location": search_term, "locale": "en_US", "limit": 50}
    response = requests.get(yelp_baseurl, params=params, headers=headers)
    text_response = response.text
    yelp_data = json.loads(text_response)
    return yelp_data


def construct_unique_key_google(google_baseurl, params):
    """
    Constructs a key that is guaranteed to uniquely and 
    repeatably identify an API request by its baseurl and params
    
    Parameters
    ----------
    google_baseurl: string
        The URL for the API endpoint
    params: dict
        A dictionary of param:value pairs
    
    Returns
    -------
    string
        the unique key as a string
    """
    google_unique_key = f"UNIQUE_KEY---{str(google_baseurl)}---{str(params)}---{str(google_secrets.google_api_key)}"

    return google_unique_key


def construct_unique_key_yelp(yelp_baseurl, params):
    ''' constructs a key that is guaranteed to uniquely and 
    repeatably identify an API request by its baseurl and params
    
    Parameters
    ----------
    yelp_baseurl: string
        The URL for the API endpoint
    params: dict
        A dictionary of param:value pairs
    
    Returns
    -------
    string
        the unique key as a string
    '''
    yelp_unique_key = f"UNIQUE_KEY---{str(yelp_baseurl)}---{str(params)}---{str(yelp_secrets.yelp_api_key)}"

    return yelp_unique_key


def load_cache(CACHE_FILE_NAME):
    """
    Opens the cache file if it exists and loads the JSON into
    the cache dictionary.
    if the cache file doesn't exist, creates a new cache dictionary.
    
    Parameters
    ----------
    None
    
    Returns
    -------
    The opened cache: dict
    """
    try:
        cache_file = open(CACHE_FILE_NAME, 'r')
        cache_file_contents = cache_file.read()
        cache = json.loads(cache_file_contents)
    except:
        cache = {}
    return cache


def save_cache(cache, CACHE_FILE_NAME):
    '''
    Saves the current state of the cache.
    
    Parameters
    ----------
    cache
        The dictionary to save.
    CACHE_FILE_NAME
        The name of the file to which
        to save the cache.
    
    Returns
    -------
    None
    '''
    cache_file = open(CACHE_FILE_NAME, 'w')
    contents_to_write = json.dumps(cache)
    cache_file.write(contents_to_write)
    cache_file.close()


def make_google_request_using_cache(google_baseurl, search_term):
    """
    Check the Google cache for a saved result with this unique_key. 
    If the result is found, return it. 
    Otherwise send a new request, save it, then return it.
    
    Parameters
    ----------
    google_baseurl: string
        The URL for the API endpoint
    search_term:
        The search term provided by user input.
    
    Returns
    -------
    CACHE_DICT[google_unique_key]
        the results of the query as a dictionary loaded from cache
        JSON
    """
    CACHE_DICT = load_cache(GOOGLE_CACHE_FILE_NAME)
    params = {"query": search_term, "key": google_secrets.google_api_key, "language": language, "type": place_type}
    google_unique_key = construct_unique_key_google(google_baseurl, params)

    if google_unique_key in CACHE_DICT.keys():
        print("\nUsing Google cache\n")
        return CACHE_DICT[google_unique_key]
    else:
        print("\nFetching from Google\n")
        CACHE_DICT[google_unique_key] = fetch_google_data(google_baseurl, search_term)
        save_cache(CACHE_DICT, GOOGLE_CACHE_FILE_NAME)
        return CACHE_DICT[google_unique_key]


def make_yelp_request_using_cache(yelp_baseurl, search_term):
    """
    Check the Yelp cache for a saved result with this unique_key. 
    If the result is found, return it. 
    Otherwise send a new request, save it, then return it.
    
    Parameters
    ----------
    yelp_baseurl: string
        The URL for the API endpoint
    search_term:
        The search term provided by user input.
    
    Returns
    -------
    CACHE_DICT[yelp_unique_key]
        the results of the query as a dictionary loaded from cache
        JSON
    """
    CACHE_DICT = load_cache(YELP_CACHE_FILE_NAME)
    search_term = f"{city_term}, {state_term}"
    params = {"categories": category, "location": search_term, "locale": "en_US", "limit": 50}
    yelp_unique_key = construct_unique_key_yelp(yelp_baseurl, params)

    if yelp_unique_key in CACHE_DICT.keys():
        print("\nUsing Yelp cache\n")
        return CACHE_DICT[yelp_unique_key]
    else:
        print("\nFetching from Yelp\n")
        CACHE_DICT[yelp_unique_key] = fetch_yelp_data(yelp_baseurl, search_term)
        save_cache(CACHE_DICT, YELP_CACHE_FILE_NAME)
        return CACHE_DICT[yelp_unique_key]


drop_google_rating_info = '''
    DROP TABLE IF EXISTS "Google Rating Info";
'''

create_google_rating_info = '''
    CREATE TABLE IF NOT EXISTS "Google_Rating_Info" (
        'place_id' TEXT PRIMARY KEY,
        'name' TEXT,
        'formatted address' TEXT,
        'rating' FLOAT NOT NULL,
        'user_ratings_total' INTEGER NOT NULL
    );
'''

drop_google_price_info = '''
    DROP TABLE IF EXISTS "Google Price Info";
'''

create_google_price_info = '''
    CREATE TABLE IF NOT EXISTS "Google_Price_Info" (
        'place_id' TEXT,
        'name' TEXT,
        'formatted address' TEXT,
        'price_level' TEXT,
        FOREIGN KEY (place_id) REFERENCES Google_Rating_Info (place_id)
    );
'''

drop_yelp_rating_info = '''
    DROP TABLE IF EXISTS "Yelp_Rating_Info";
'''

create_yelp_rating_info = '''
    CREATE TABLE IF NOT EXISTS "Yelp_Rating_Info" (
        'id' TEXT PRIMARY KEY,
        'alias'  TEXT,
        'name' TEXT,
        'display_address' TEXT,
        'rating' FLOAT NOT NULL,
        'review_count' TEXT NOT NULL
    );
'''

drop_yelp_price_info = '''
    DROP TABLE IF EXISTS "Yelp_Price_Info";
'''

create_yelp_price_info = '''
    CREATE TABLE IF NOT EXISTS "Yelp_Price_Info" (
        'id' TEXT,
        'alias'  TEXT,
        'name' TEXT,
        'display_address' TEXT,
        'phone' TEXT,
        'price' TEXT NOT NULL,
        FOREIGN KEY (id) REFERENCES Yelp_Rating_Info (id)
    );
'''

insert_google_rating_info = '''
    INSERT INTO Google_Rating_Info
    VALUES (?, ?, ?, ?, ?)
'''

insert_google_price_info = '''
    INSERT INTO Google_Price_Info
    VALUES (?, ?, ?, ?)
'''

insert_yelp_rating_info = '''
    INSERT INTO Yelp_Rating_Info
    VALUES (?, ?, ?, ?, ?, ?)
'''

insert_yelp_price_info = '''
    INSERT INTO Yelp_Price_Info
    VALUES (?, ?, ?, ?, ?, ?)
'''


cur.execute(drop_google_rating_info)
cur.execute(create_google_rating_info)
cur.execute(drop_google_price_info)
cur.execute(create_google_price_info)

cur.execute(drop_yelp_rating_info)
cur.execute(create_yelp_rating_info)
cur.execute(drop_yelp_price_info)
cur.execute(create_yelp_price_info)

conn.commit()

if __name__ == "__main__":

    GOOGLE_CACHE_DICT = load_cache(GOOGLE_CACHE_FILE_NAME)
    YELP_CACHE_DICT = load_cache(YELP_CACHE_FILE_NAME)

    while True:

        google_baseurl = "https://maps.googleapis.com/maps/api/place/textsearch/json?"
        yelp_baseurl = "https://api.yelp.com/v3/businesses/search"
        category = "restaurants, All"

        city_term = input("\nEnter U.S. city name WITHOUT state (e.g. 'Ann Arbor'), or 'exit program' to quit: ")

        city_term = city_term.lower()

        if city_term == 'exit program':
            quit()
        
        else:

            state_term = input("\nEnter full U.S. state name corresponding to city above (e.g. 'Michigan'), or 'exit program' to quit: ")

            if state_term.lower() == 'exit program':
                quit()

            elif state_term.lower() not in states:
                print("\n[Error] Invalid state name. Please enter your city and state terms again, or start a new search.\n")
                continue

            elif state_term.lower() in states:
                state_term = state_term.lower()
                search_term = f"{city_term}, {state_term}"
                language = "en"
                place_type = "restaurant"
                google_data = make_google_request_using_cache(google_baseurl, search_term)
                print(google_data)
                print("\n\n\n")
                print(len(google_data["results"])) 
                print("\n\n\n")
                yelp_data = make_yelp_request_using_cache(yelp_baseurl, search_term)
                print(yelp_data)
                print("\n\n\n")
                print(len(yelp_data["businesses"])) 
                print("\n\n\n")

                google_data_for_ratings_info = []
                google_data_for_price_info = []

                yelp_data_for_ratings_info = []
                yelp_data_for_price_info = []

                for result in google_data["results"]:
                    place_id = result["place_id"]
                    name = result["name"]
                    formatted_address = result["formatted_address"]
                    rating = result["rating"]
                    user_ratings_total = result["user_ratings_total"]
                    try:
                        price_level = result["price_level"]
                    except:
                        price_level = "N/A"
                    google_data_for_ratings_info.append([place_id, name, formatted_address, rating, user_ratings_total])
                    google_data_for_price_info.append([place_id, name, formatted_address, price_level])
    

                for business in yelp_data["businesses"]:
                    id_string = business["id"]
                    alias = business["alias"]
                    name = business["name"]
                    try:
                        display_address = str(business["location"]["display_address"][0]) + " " + str(business["location"]["display_address"][1])
                    except:
                        display_address = "N/A"
                    rating = business["rating"]
                    review_count = business["review_count"]
                    phone = business["phone"]
                    price = business["price"]
                    yelp_data_for_ratings_info.append([id_string, alias, name, display_address, rating, review_count])
                    yelp_data_for_price_info.append([id_string, alias, name, display_address, phone, price])


                for result in google_data_for_ratings_info:
                    print("\n Inserting " + result[1] + " ...\n")
                    cur.execute(insert_google_rating_info, result)
                
                for result in google_data_for_price_info:
                    print("\n Inserting " + result[1] + " ...\n")
                    cur.execute(insert_google_price_info, result)

                for business in yelp_data_for_ratings_info:
                    print("\n Inserting " + business[2] + " ...\n")
                    cur.execute(insert_yelp_rating_info, business)

                for business in yelp_data_for_price_info:
                    print("\n Inserting " + business[2] + " ...\n")
                    cur.execute(insert_yelp_price_info, business)
                
                conn.commit()

                continue




