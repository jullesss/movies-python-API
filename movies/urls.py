from django.urls import path
from .views import MovieView, SpecificMovieView, MovieOrderView

urlpatterns = [
    path("movies/", MovieView.as_view()),
    path("movies/<int:movie_id>/", SpecificMovieView.as_view()),
    path("movies/<int:movie_id>/orders/", MovieOrderView.as_view()),
]
