from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from account.models import CustomUser

# Получаем модель пользователя, указанную в настройках проекта.
User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели User, используется для представления пользователей без пароля.
    """
    class Meta:
        model = User
        exclude = ('password',)  # Исключаем поле password из сериализации.


class RegisterSerializer(serializers.ModelSerializer):
    """
    Сериализатор для регистрации новых пользователей.

    Аргументы:
    - password (str): Пароль пользователя.
    - password2 (str): Подтверждение пароля (должно совпадать с password).

    Примечание:
    - При создании пользователя проверяет, что пароль и подтверждение пароля совпадают
      и соответствуют требованиям для пароля (минимальная и максимальная длина).
    """
    password = serializers.CharField(min_length=8, max_length=20, required=True, write_only=True)
    password2 = serializers.CharField(min_length=8, max_length=20, required=True, write_only=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'password2', 'first_name', 'last_name', 'avatar', 'username')

    def validate(self, attrs):
        """
        Проверка валидности данных сериализатора.
        """
        password = attrs['password']
        password2 = attrs.pop('password2')
        if password2 != password:
            raise serializers.ValidationError('Passwords didn\'t match!')
        validate_password(password)  # Проверяем, что пароль соответствует требованиям.
        return attrs

    def create(self, validated_data):
        """
        Создание нового пользователя на основе валидированных данных.
        """
        user = User.objects.create_user(**validated_data)
        return user


class ChangePasswordSerializer(serializers.Serializer):
    """
    Сериализатор для изменения пароля пользователя.

    Аргументы:
    - old_password (str): Текущий пароль пользователя.
    - new_password (str): Новый пароль, на который необходимо изменить текущий пароль.

    Примечание:
    - Сериализатор не связан с моделью User, поэтому не используем Meta класс.
    """
    model = User

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

# from django.contrib.auth import get_user_model
# from django.contrib.auth.password_validation import validate_password
# from django.contrib.auth.models import User
# from rest_framework import serializers
#
# from account.models import CustomUser
#
# # import logging
# #
# # logger = logging.getLogger('main')
#
# User = get_user_model()
#
#
# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         exclude = ('password',)
#
#
# class RegisterSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(min_length=8, max_length=20,
#                                      required=True, write_only=True)
#     password2 = serializers.CharField(min_length=8, max_length=20,
#                                       required=True, write_only=True)
#
#     class Meta:
#         model = User
#         fields = ('email', 'password', 'password2', 'first_name', 'last_name',
#                   'avatar', 'username')
#
#     def validate(self, attrs):
#         password = attrs['password']
#         password2 = attrs.pop('password2')
#         if password2 != password:
#             raise serializers.ValidationError('Passwords didn\'t match!')
#         validate_password(password)
#         return attrs
#
#     def create(self, validated_data):
#         user = User.objects.create_user(**validated_data)
#         return user
#
#
# class ChangePasswordSerializer(serializers.Serializer):
#     model = User
#
#     """
#     Serializer for password change endpoint.
#     """
#     old_password = serializers.CharField(required=True)
#     new_password = serializers.CharField(required=True)
