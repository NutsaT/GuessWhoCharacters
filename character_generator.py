

import requests
import os,random
from datetime import datetime
# from db import get_db_connection




TMDB_SEARCH_URL = "https://api.themoviedb.org/3/search/person"
TMDB_PERSON_DETAILS = "https://api.themoviedb.org/3/person/{}"
TMDB_IMAGE_BASE = "https://image.tmdb.org/t/p/w500"


project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
API_KEY = "d7eb157cef3f8e59b4521511bcd2f37c"


TMDB_SEARCH_MOVIE_URL = "https://api.themoviedb.org/3/search/movie"
TMDB_MOVIE_DETAILS_URL = "https://api.themoviedb.org/3/movie/{}"
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))




# def get_random_movie():
#     while True:
#         random_year = random.randint(1970, 2024)
#         print(f"Searching for a movie from the year {random_year}...")


#         for page in random.sample(range(1, 50), 5):
#             url = (
#                 f'https://api.themoviedb.org/3/discover/movie?api_key={API_KEY}'
#                 f'&language=en-US&sort_by=vote_count.desc&page={page}'
#                 f'&primary_release_year={random_year}'
#                 f'&vote_count.gte=5000'
#             )
#             response = requests.get(url)
#             if response.status_code != 200:
#                 continue


#             data = response.json()
#             if 'results' not in data or not data['results']:
#                 continue


#             random.shuffle(data['results'])
#             for movie_data in data['results']:
#                 movie_id = movie_data['id'] 
#                 return movie_data


# def main():
#     movie_data = get_random_movie()
#     movie_name = movie_data['original_title']
#     movie_id = movie_data['id']


#     print(f"Selected movie: {movie_name} (TMDb ID: {movie_id})")
#     return movie_data, movie_name, movie_id






# def get_cast(movie_id):
#     url = f'https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key={API_KEY}'
#     response = requests.get(url)
#     data = response.json()
#     return data['cast']


# # print(get_cast(550))


# def return_actors():
#     # Get the cast for the selected movie
#     movie_data, movie_name, movie_id, nicknames = main()
#     cast_list = get_cast(movie_data['id'])


#     # Extract the first 10 actor names
#     actor_names = [actor['name'] for actor in cast_list[:10]]
#     movie_name = movie_name
#     actor_names = actor_names[::-1]
#     print(f"Movie: {movie_data['original_title']}")
#     print(f"Actors: {actor_names}")
#     return actor_names, movie_id, movie_name, nicknames




# def fetch_actor_image(actor_name):
#     search_params = {
#         "api_key": API_KEY,
#         "query": actor_name
#     }
#     search_response = requests.get(TMDB_SEARCH_URL, params=search_params)
#     if search_response.status_code != 200:
#         print(f"Error searching for {actor_name}")
#         return None


#     results = search_response.json().get("results", [])
#     if not results:
#         print(f"No results found for {actor_name}")
#         return None


#     actor_id = results[0]["id"]


#     details_response = requests.get(TMDB_PERSON_DETAILS.format(actor_id), params={"api_key": API_KEY})
#     if details_response.status_code != 200:
#         print(f"Error getting details for {actor_name}")
#         return None


#     profile_path = details_response.json().get("profile_path")
#     if not profile_path:
#         print(f"No profile image for {actor_name}")
#         return None


#     return f"{TMDB_IMAGE_BASE}{profile_path}"






# def fetch_movie_details(movie_index):
#     search_params = {
#         "api_key": API_KEY,
#         "query": movie_index
#     }
#     search_response = requests.get(TMDB_SEARCH_MOVIE_URL, params=search_params)
#     if search_response.status_code != 200:
#         print(f"Error searching for movie '{movie_index}'")
#         return None


#     results = search_response.json().get("results", [])
#     if not results:
#         print(f"No results found for movie '{movie_index}'")
#         return None


#     movie_data = results[0]
#     movie_id = movie_data["id"]


#     details_response = requests.get(TMDB_MOVIE_DETAILS_URL.format(movie_id), params={"api_key": API_KEY})
#     if details_response.status_code != 200:
#         print(f"Error fetching details for movie'")
#         return None


#     details = details_response.json()
#     genre_list = [g["name"] for g in details.get("genres", [])]
#     genre_str = ", ".join(genre_list)
#     release_year = int(details["release_date"][:4]) if "release_date" in details else None
#     summary = details.get("overview", "")
#     poster_path = details.get("poster_path")
#     poster_url = f"{TMDB_IMAGE_BASE}{poster_path}" if poster_path else ""


#     return genre_str, release_year, summary, poster_url, movie_id




# def get_or_create_actor(cursor, actor_name, image_url):
#     cursor.execute("SELECT actor_id FROM actors WHERE actor_name = %s", (actor_name,))
#     result = cursor.fetchone()
#     if result:
#         return result[0]
#     else:
#         cursor.execute(
#             "INSERT INTO actors (actor_name, image_url) VALUES (%s, %s)",
#             (actor_name, image_url)
#         )
#         return cursor.lastrowid


# def insert_movie(cursor, movie_index,movie_name):


#     url = f"https://api.themoviedb.org/3/movie/{movie_index}?api_key={API_KEY}"
#     response = requests.get(url)


#     if response.status_code != 200:
#         genre, release_year, summary, poster_url, idx = "", None, "", "", movie_index
#     else:
#         data = response.json()


#         genre_list = [g["name"] for g in data.get("genres", [])]
#         genre = ", ".join(genre_list)


#         release_year = int(data["release_date"][:4]) if data.get("release_date") else None
#         summary = data.get("overview", "")
#         poster_path = data.get("poster_path")
#         poster_url = f"{TMDB_IMAGE_BASE}{poster_path}" if poster_path else ""


#         idx = movie_index  # 🔥 IMPORTANT: keep original ID




#     cursor.execute("""
#         INSERT INTO movies (
#         movie_name, idx, timestamp, genre, release_year, summary, poster_url
#         ) VALUES (%s,%s, %s, %s, %s, %s, %s)
#     """, (movie_name, idx, datetime.now(), genre, release_year, summary, poster_url))
#     movie_id = cursor.lastrowid
#     print(movie_id)
#     return movie_id




# def link_actor_to_movie(cursor, movie_id, actor_id, position):
#     cursor.execute("""
#         INSERT INTO movie_cast (movie_id, actor_id, position)
#         VALUES (%s, %s, %s)
#         ON DUPLICATE KEY UPDATE position=VALUES(position)
#     """, (movie_id, actor_id, position))


# def fetch_images_and_save_to_db():
#     db = get_db_connection()
#     cursor = db.cursor()
#     actor_names, movie_index, movie_name, nicknames = return_actors()


#     # Insert movie
#     movie_id = insert_movie(cursor, movie_index,movie_name)
  
#     for pos, actor_name in enumerate(actor_names):
#         image_url = fetch_actor_image(actor_name) or ""
#         actor_id = get_or_create_actor(cursor, actor_name, image_url)
#         link_actor_to_movie(cursor, movie_id, actor_id, pos)


#     db.commit()
#     print(f"Movie '{movie_name}' and {len(actor_names)} actors saved to DB.")




# def get_all_movies():
#     db = get_db_connection()
#     cursor = db.cursor(dictionary=True)
#     cursor.execute("SELECT * FROM movies")
#     movies = cursor.fetchall()
#     cursor.close()
#     db.close()
#     return movies


# def get_recent_movies(n=10):
#     db = get_db_connection()
#     cursor = db.cursor(dictionary=True)
#     cursor.execute("SELECT * FROM movies ORDER BY timestamp DESC LIMIT %s", (n,))
#     recent = cursor.fetchall()
#     cursor.close()
#     db.close()
#     return recent






# # Run your data insertion
# # fetch_images_and_save_to_db()




import random, json


def get_movie_by_popularity():
   random_page = random.randint(1,5)
   url = f'https://api.themoviedb.org/3/discover/movie?api_key={API_KEY}&page={random_page}&language=en-US&vote_count.gte=5000&sort_by=popularity.desc'
  
   response = requests.get(url)
   data = response.json()
   count_per_page = len(data["results"])
   random_int = random.randint(1, count_per_page-1)


   print("random int",random_int)
   print("count",count_per_page)
   film = data["results"][random_int]


   print(film['id'])
   return film['id'], film['title']






def get_a_character():
   movie_id,movie_title=get_movie_by_popularity()
   url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key={API_KEY}"


   response = requests.get(url)
   data = response.json()['cast']
   # pretty_json = json.dumps(data, indent=1)
   character_names = [character['character'] for character in data[:3]]
   random_character = random.choice(character_names)


   print(random_character)
   return random_character,movie_title
# get_a_character()


import requests
from urllib.parse import quote
import requests
from urllib.parse import quote
from ddgs import DDGS


def get_image():
    try:
        character_name_unchanged, movie_title = get_a_character()

        character_name = (
            f'"{character_name_unchanged}" FICTIONAL CHARACTER "{movie_title}" '
        )
        character_name_unchanged += f" ({movie_title})"

        print("\n\nCHARACTER NAME:",character_name)
        # if "(voice)" in character_name:
        #     character_name = character_name.replace("(voice)", "")

        results = DDGS().images(
            query=character_name,
            max_results=10,
            backend="google"
        )

        for result in results:
            image_url = result["image"]

            try:
                response = requests.get(
                    image_url,
                    timeout=5,
                    stream=True
                )

                if response.status_code == 200:
                    print("Working image:", image_url)
                    return image_url, character_name_unchanged

                print("Broken image:", image_url, response.status_code)

            except requests.RequestException as e:
                print("Image failed:", image_url, e)

        print("No working images found")
        return None

    except Exception as e:
        print("Image search failed:", e)
        return None

# image_url = get_wikipedia_image(character_name)


# print(get_image(character_name))

