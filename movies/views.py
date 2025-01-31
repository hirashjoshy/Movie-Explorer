from django.shortcuts import render
from django.shortcuts import redirect
from django.core.cache import cache
from django.conf import settings
from django.contrib import messages
import requests 
from math import ceil

# Create your views here.


## Cache has been implemented in all the functions

def home(request):
    trending_movies = [
        "Batman", "Avengers", "Inception", "Titanic", "Interstellar", 
        "The Matrix", "The Godfather", "Jurassic Park", 
        "Forrest Gump", "The Dark Knight", "Pulp Fiction", "Gladiator"
    ]  

    movies_data = []

    for title in trending_movies:
        cache_key = f"movie_{title}"  # Creating a cache key for each Movie
        movie_data = cache.get(cache_key)

        if not movie_data:  # Fetch from API only if cache key is not present
            response = requests.get("https://www.omdbapi.com/", params={"apikey": settings.OMDB_API_KEY, "t": title})
            data = response.json()

            if response.status_code == 200 and data.get("Response") == "True":
                movie_data = data
                cache.set(cache_key, movie_data, timeout=3600)  # Cache for 1 hour

        if movie_data:
            movies_data.append(movie_data)

    return render(request, "movies/home.html", {"movies": movies_data})

import logging 

logger = logging.getLogger(__name__)

def search(request):
    query = request.GET.get("q", "").strip()
    page = int(request.GET.get("page", 1))  
    results_per_page = 10
    total_pages = 0  

    # Create a cache key based on the query and page number
    cache_key = f"search_{query}_page_{page}"

    # Try to get the results from the cache
    cached_movies = cache.get(cache_key)
    
    if cached_movies is not None:
        logger.debug(f"Using cached results for query '{query}' and page {page}")
        movies = cached_movies
        total_pages = int(request.GET.get("total_pages", 0))  
    else:
        logger.debug(f"Making API call for page {page} with query '{query}'")
        response = requests.get("https://www.omdbapi.com/", params={
            "apikey": settings.OMDB_API_KEY, 
            "s": query, 
            "page": page
        })
        data = response.json()

        if data.get("Response") == "True":
            total_results = int(data.get("totalResults", 0))
            movies = data.get("Search", [])

            total_pages = ceil(total_results / results_per_page)

            cache.set(cache_key, movies, timeout=1800) 

            logger.debug(f"API returned {len(movies)} movies for page {page}")
            logger.debug(f"Total pages: {total_pages}")
        else:
            logger.error(f"Error fetching data from OMDB: {data.get('Error', 'Unknown error')}")
            movies = []  

    
    previous_page = max(1, page - 1)  
    next_page = min(total_pages, page + 1)  

    return render(request, "movies/search.html", {
        "movies": movies,
        "query": query,
        "page": page,
        "total_pages": total_pages,
        "previous_page": previous_page,
        "next_page": next_page,
    })


def movie_details(request, imdb_id):
    cache_key = f"movie_{imdb_id}"  
    movie = cache.get(cache_key)

    if not movie:  
        response = requests.get("https://www.omdbapi.com/", params={"apikey": settings.OMDB_API_KEY, "i": imdb_id})
        movie = response.json()

        if movie.get("Response") == "True":
            cache.set(cache_key, movie, timeout=86400) 

    return render(request, "movies/details.html", {"movie": movie})

def add_to_favorites(request, imdb_id):
    if 'favorites' not in request.session:
        request.session['favorites'] = []

    if imdb_id not in request.session['favorites']:
        request.session['favorites'].append(imdb_id)
        request.session.modified = True
        messages.success(request, "Movie added to your favorites!")

    return redirect('movie_details', imdb_id=imdb_id)

def remove_from_favorites(request, imdb_id):
    favorites = request.session.get('favorites', [])

    if imdb_id in favorites:
        favorites.remove(imdb_id)

    request.session['favorites'] = favorites
    request.session.modified = True

    return redirect('favorites')

def favorites_list(request):
    favorite_ids = request.session.get('favorites', [])
    favorite_movies = []

    for imdb_id in favorite_ids:
        cache_key = f"movie_{imdb_id}"
        movie = cache.get(cache_key)

        if not movie:  
            response = requests.get("https://www.omdbapi.com/", params={"apikey": settings.OMDB_API_KEY, "i": imdb_id})
            movie = response.json()
            if movie.get("Response") == "True":
                cache.set(cache_key, movie, timeout=86400)  
        if movie:
            favorite_movies.append(movie)

    return render(request, "movies/favorites.html", {"movies": favorite_movies})