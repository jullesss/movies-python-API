from rest_framework.views import APIView, Request, Response, status
from users.models import User
from users.serializers import UserSerializer
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import (
    IsAuthenticated,
)
from .permissions import IsAdminOrOwner


class UserView(APIView):
    def get(self, request: Request) -> Response:
        users = User.objects.all()

        serializer = UserSerializer(users, many=True)

        return Response(serializer.data, status.HTTP_200_OK)

    def post(self, request: Request) -> Response:
        serializer = UserSerializer(data=request.data)  # type: ignore

        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(serializer.data, status.HTTP_201_CREATED)


class UserDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    # Leitura da esquerda para a direita
    # Quando é separado por virgula, ambas as condicionais precisam ser verdadeiras
    # Quando separado por pipe (|), apenas uma das condinais precisa ser verdadeira
    # permission_classes = [IsBookOwner | IsAdminOrReadOnly]
    permission_classes = [IsAuthenticated, IsAdminOrOwner]

    def get(self, request: Request, user_id=int) -> Response:
        user = get_object_or_404(User, pk=user_id)

        serializer = UserSerializer(user)

        return Response(serializer.data, status.HTTP_200_OK)

    def patch(self, request: Request, user_id=int) -> Response:
        user = get_object_or_404(User, pk=user_id)
        self.check_object_permissions(request, user)

        serializer = UserSerializer(instance=user, data=request.data, partial=True)  # type: ignore

        serializer.is_valid(raise_exception=True)

        serializer.save()  # type: ignore

        return Response(serializer.data, status.HTTP_200_OK)
