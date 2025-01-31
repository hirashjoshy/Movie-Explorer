from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search, name='search'),
    path('movie/<str:imdb_id>/', views.movie_details, name='movie_details'),
]