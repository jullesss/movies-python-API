from django.urls import path
from .views import UserView, UserDetailView
from movies.views import LoginView

urlpatterns = [
    path("users/", UserView.as_view()),
    path("users/<int:user_id>/", UserDetailView.as_view()),
    path("users/login/", LoginView.as_view()),
]
