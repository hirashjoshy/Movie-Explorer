from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search, name='search'),
    path('movie/<str:imdb_id>/', views.movie_details, name='movie_details'),
    path('favorites/', views.favorites_list, name='favorites'),
    path('add-to-favorites/<str:imdb_id>/', views.add_to_favorites, name='add_to_favorites'),
    path('remove-from-favorites/<str:imdb_id>/', views.remove_from_favorites, name='remove_from_favorites'),
]