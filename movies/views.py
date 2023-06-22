from rest_framework.views import APIView, Request, Response, status
from movies.models import Movie
from movies.serializers import MovieSerializer, MovieOrderSerializer
from users.serializers import LoginSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import (
    IsAuthenticated,
)
from users.permissions import IsAdminOrReadOnly
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken


class LoginViewOld(APIView):
    def post(self, request: Request) -> Response:  # type: ignore
        serializer = LoginSerializer(data=request.data)  # type: ignore
        serializer.is_valid(raise_exception=True)  # type: ignore

        user = authenticate(**serializer.validated_data)  # type: ignore

        if not user:
            return Response(
                {"detail": "No active account found with the given credentials"},
                status.HTTP_401_UNAUTHORIZED,
            )

        refresh = RefreshToken.for_user(user)

        token_dict = {"refresh": str(refresh), "access": str(refresh.access_token)}

        return Response(token_dict, status.HTTP_200_OK)


class MovieView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request: Request) -> Response:
        movies = Movie.objects.all()

        serializer = MovieSerializer(movies, many=True)

        return Response(serializer.data, status.HTTP_200_OK)

    def post(self, request: Request) -> Response:
        serializer = MovieSerializer(data=request.data)  # type: ignore

        serializer.is_valid(raise_exception=True)

        serializer.save(user=request.user)

        return Response(serializer.data, status.HTTP_201_CREATED)


class SpecificMovieView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request: Request, movie_id=int) -> Response:
        movie = get_object_or_404(Movie, id=movie_id)

        serializer = MovieSerializer(instance=movie)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def delete(self, request: Request, movie_id: int) -> Response:
        movie = get_object_or_404(Movie, id=movie_id)
        movie.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class MovieOrderView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request: Request, movie_id: int) -> Response:
        movie_obj = get_object_or_404(Movie, pk=movie_id)
        self.check_object_permissions(request, movie_obj)
        serializer = MovieOrderSerializer(data=request.data)  # type: ignore

        serializer.is_valid(raise_exception=True)

        serializer.save(user=request.user, movie=movie_obj)

        return Response(serializer.data, status.HTTP_201_CREATED)
