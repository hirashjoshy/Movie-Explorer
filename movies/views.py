from django.shortcuts import render
from django.core.cache import cache
from django.conf import settings
import requests 

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

def search(request):
    query = request.GET.get("q", "").strip()
    cache_key = f"search_{query}"  
    movies = cache.get(cache_key)

    if query and not movies:  
        response = requests.get("https://www.omdbapi.com/", params={"apikey": settings.OMDB_API_KEY, "s": query})
        data = response.json()

        if data.get("Response") == "True":
            movies = data.get("Search", [])
            cache.set(cache_key, movies, timeout=1800)  # Cache for 30 minutes

    return render(request, "movies/search.html", {"movies": movies or [], "query": query})

def movie_details(request, imdb_id):
    cache_key = f"movie_{imdb_id}"  
    movie = cache.get(cache_key)

    if not movie:  
        response = requests.get("https://www.omdbapi.com/", params={"apikey": settings.OMDB_API_KEY, "i": imdb_id})
        movie = response.json()

        if movie.get("Response") == "True":
            cache.set(cache_key, movie, timeout=86400) 

    return render(request, "movies/details.html", {"movie": movie})