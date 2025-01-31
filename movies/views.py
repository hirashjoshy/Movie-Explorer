from django.shortcuts import render
from django.shortcuts import redirect
from django.core.cache import cache
from django.conf import settings
from django.contrib import messages
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

def add_to_favorites(request, imdb_id):
    if 'favorites' not in request.session:
        request.session['favorites'] = []

    if imdb_id not in request.session['favorites']:
        request.session['favorites'].append(imdb_id)
        request.session.modified = True
        messages.success(request, "Movie added to your favorites!")

    return redirect('movie_details', imdb_id=imdb_id)

def remove_from_favorites(request, imdb_id):
    # Get the current list of favorites from the session
    favorites = request.session.get('favorites', [])

    # Remove the movie from the favorites list if it exists
    if imdb_id in favorites:
        favorites.remove(imdb_id)

    # Save the updated favorites list back to the session
    request.session['favorites'] = favorites
    request.session.modified = True

    # Redirect back to the favorites page
    return redirect('favorites')

def favorites_list(request):
    # Get the list of favorite movie IDs from the session
    favorite_ids = request.session.get('favorites', [])
    favorite_movies = []

    # Fetch details for each favorite movie using the API
    for imdb_id in favorite_ids:
        cache_key = f"movie_{imdb_id}"
        movie = cache.get(cache_key)

        if not movie:  # If not in cache, fetch from API
            response = requests.get("https://www.omdbapi.com/", params={"apikey": settings.OMDB_API_KEY, "i": imdb_id})
            movie = response.json()
            if movie.get("Response") == "True":
                cache.set(cache_key, movie, timeout=86400)  # Cache for 1 day
        if movie:
            favorite_movies.append(movie)

    return render(request, "movies/favorites.html", {"movies": favorite_movies})