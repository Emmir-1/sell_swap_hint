from django.contrib.auth import get_user_model
from django.urls import path
from django.views.decorators.cache import cache_page
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, SAFE_METHODS
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, UpdateModelMixin
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import generics
from rest_framework.response import Response

from rest_framework import status
from django.contrib.auth.models import User

from product.permissions import IsAuthor
from product.serializers import FavoriteListSerializer
from .serializers import ChangePasswordSerializer
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from account import serializers
from account.send_mail import send_confirmation_email

User = get_user_model()


class UserViewSet(ListModelMixin, UpdateModelMixin, GenericViewSet):
    """
    Представление пользователей с возможностью просмотра списка и обновления профиля.

    Аргументы:
    - queryset (QuerySet): QuerySet, который определяет набор объектов для представления.
    - serializer_class (Serializer): Сериализатор для преобразования данных пользователя.

    Примечание:
    - Представление позволяет просматривать список пользователей и обновлять свой профиль.
    - Разрешает обновление профиля только авторизованным пользователям.
    """
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer

    def get_permissions(self):
        """
        Возвращает список прав для каждого действия представления.
        """
        if self.action in ('update', 'partial_update'):  # PUT и PATCH
            return (IsAuthor(),)  # Разрешено только автору профиля.
        return (AllowAny(),)  # Разрешено всем.

    @action(['POST'], detail=False)
    def register(self, request, *args, **kwargs):
        """
        Метод для регистрации новых пользователей.

        Аргументы:
        - request (Request): Объект запроса, содержащий данные пользователя.
        """
        serializer = serializers.RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        if user:
            try:
                send_confirmation_email(user.email, user.activation_code)
            except Exception as e:
                return Response({'msg': 'Registered, but troubles with email!',
                                 'data': serializer.data}, status=201)
        return Response(serializer.data, status=201)

    @action(['GET'], detail=False, url_path='activate/(?P<uuid>[0-9A-Fa-f-]+)')
    def activate(self, request, uuid):
        """
        Метод для активации пользователя по уникальному коду активации.

        Аргументы:
        - request (Request): Объект запроса.
        - uuid (str): Уникальный код активации пользователя.
        """
        try:
            user = User.objects.get(activation_code=uuid)
        except User.DoesNotExist:
            return Response({'msg': 'Invalid link or link expired!'}, status=400)
        user.is_active = True
        user.activation_code = ''
        user.save()
        return Response({'msg': 'User successfully activated!'}, status=200)

    # @cache_page(60 * 15)
    @action(['GET'], detail=True)
    def favorites(self, request, pk):
        """
        Метод для получения списка избранных продуктов пользователя.

        Аргументы:
        - request (Request): Объект запроса.
        - pk (int): Идентификатор пользователя.

        Примечание:
        - Позволяет получить список избранных продуктов для указанного пользователя.
        """
        product = self.get_object()
        favorites = product.favorites.filter(favorite=True)
        serializer = FavoriteListSerializer(instance=favorites, many=True)
        return Response(serializer.data, status=200)


class LoginView(TokenObtainPairView):
    """
    Представление для получения токена доступа (авторизации).

    Примечание:
    - Разрешено всем пользователям.
    """
    permission_classes = (AllowAny,)


class RefreshView(TokenRefreshView):
    """
    Представление для обновления токена доступа.

    Примечание:
    - Разрешено всем пользователям.
    """
    permission_classes = (AllowAny,)


class ChangePasswordView(generics.UpdateAPIView):
    """
    Представление для изменения пароля пользователя.

    Аргументы:
    - serializer_class (Serializer): Сериализатор для изменения пароля.
    - model (Model): Модель пользователя (User).
    - permission_classes (list): Список прав доступа (только для аутентифицированных пользователей).

    Примечание:
    - Разрешено только аутентифицированным пользователям.
    """
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        """
        Возвращает объект пользователя (себя) для обновления пароля.
        """
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        """
        Метод для обновления пароля пользователя.

        Аргументы:
        - request (Request): Объект запроса, содержащий данные для изменения пароля.
        """
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# from django.contrib.auth import get_user_model
# from django.urls import path
# from django.views.decorators.cache import cache_page
# from rest_framework.decorators import action
# from rest_framework.permissions import AllowAny, SAFE_METHODS
# from rest_framework.viewsets import GenericViewSet
# from rest_framework.mixins import ListModelMixin, UpdateModelMixin
# from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
# from rest_framework import generics
# from rest_framework.response import Response
#
# from rest_framework import status
# from django.contrib.auth.models import User
#
# from product.permissions import IsAuthor
# from product.serializers import FavoriteListSerializer
# from .serializers import ChangePasswordSerializer
# from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
#
# from account import serializers
# from account.send_mail import send_confirmation_email
#
# # from favorite.serializers import FavoriteUserSerializer
#
# User = get_user_model()
#
#
# class UserViewSet(ListModelMixin, UpdateModelMixin, GenericViewSet):
#     queryset = User.objects.all()
#     serializer_class = serializers.UserSerializer
#
#     def get_permissions(self):
#         if self.action in ('update', 'partial_update'):  # PUT и PATCH
#             return (IsAuthor(), )
#         return (AllowAny(),)
#
#     @action(['POST'], detail=False)
#     def register(self, request, *args, **kwargs):
#         serializer = serializers.RegisterSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.save()
#         if user:
#             try:
#                 send_confirmation_email(user.email, user.activation_code)
#             except Exception as e:
#                 return Response({'msg': 'Registered, but troubles with email!',
#                                  'data': serializer.data}, status=201)
#         return Response(serializer.data, status=201)
#
#     @action(['GET'], detail=False, url_path='activate/(?P<uuid>[0-9A-Fa-f-]+)')
#     def activate(self, request, uuid):
#         try:
#             user = User.objects.get(activation_code=uuid)
#         except User.DoesNotExist:
#             return Response({'msg': 'Invalid link or link expired!'}, status=400)
#         user.is_active = True
#         user.activation_code = ''
#         user.save()
#         return Response({'msg': 'User successfully activated!'}, status=200)
#
#     # @cache_page(60 * 15)
#     @action(['GET'], detail=True)
#     def favorites(self, request, pk):
#         product = self.get_object()
#         favorites = product.favorites.filter(favorite=True)
#         serializer = FavoriteListSerializer(instance=favorites, many=True)
#         return Response(serializer.data, status=200)
#
#
# class LoginView(TokenObtainPairView):
#     permission_classes = (AllowAny,)
#
#
# class RefreshView(TokenRefreshView):
#     permission_classes = (AllowAny,)
#
#
# class ChangePasswordView(generics.UpdateAPIView):
#     """
#     An endpoint for changing password.
#     """
#     serializer_class = ChangePasswordSerializer
#     model = User
#     permission_classes = (IsAuthenticated,)
#
#     def get_object(self, queryset=None):
#         obj = self.request.user
#         return obj
#
#     def update(self, request, *args, **kwargs):
#         self.object = self.get_object()
#         serializer = self.get_serializer(data=request.data)
#
#         if serializer.is_valid():
#             # Check old password
#             if not self.object.check_password(serializer.data.get("old_password")):
#                 return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
#             # set_password also hashes the password that the user will get
#             self.object.set_password(serializer.data.get("new_password"))
#             self.object.save()
#             response = {
#                 'status': 'success',
#                 'code': status.HTTP_200_OK,
#                 'message': 'Password updated successfully',
#                 'data': []
#             }
#
#             return Response(response)
#
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
