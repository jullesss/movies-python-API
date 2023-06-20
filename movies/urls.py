from django.urls import path
from .views import MovieView, SpecificMovieView

urlpatterns = [
    path("movies/", MovieView.as_view()),
    path("movies/<int:movie_id>/", SpecificMovieView.as_view()),
]
