from django.urls import path
from .views import UserView
from movies.views import LoginViewOld
from rest_framework_simplejwt.views import TokenObtainPairView


urlpatterns = [
    path("users/", UserView.as_view()),
    path("users/login/", LoginViewOld.as_view()),
]
