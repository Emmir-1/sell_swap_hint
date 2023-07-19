from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet

from promo.models import Promo
from . import serializers


class PromoViewSet(ModelViewSet):
    # Запрос всех объектов модели Promo
    queryset = Promo.objects.all()

    # Указываем, какой сериализатор использовать для преобразования объектов в JSON и обратно
    serializer_class = serializers.PromoSerializer

    def perform_create(self, serializer):
        # Устанавливаем текущего аутентифицированного пользователя в качестве владельца Promo при создании
        serializer.save(user=self.request.user)

    def get_permissions(self):
        # Возвращаем разрешения в зависимости от типа действия (action)
        if self.action in ('retrieve', 'list'):
            return [permissions.AllowAny(), ]  # Для действий retrieve и list разрешаем доступ всем
        return [permissions.IsAdminUser(), ]  # Для других действий требуем права администратора

    @method_decorator(cache_page(60))  # Кеширование ответа на 1 минуту
    def list(self, request, *args, **kwargs):
        # Возвращаем разбитый на страницы список всех объектов Promo
        return super().list(request, *args, **kwargs)

# from django.utils.decorators import method_decorator
# from django.views.decorators.cache import cache_page
# from rest_framework import permissions
# from rest_framework.viewsets import ModelViewSet
#
# from promo.models import Promo
# from . import serializers
#
#
# class PromoViewSet(ModelViewSet):
#     queryset = Promo.objects.all()
#     serializer_class = serializers.PromoSerializer
#
#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)
#
#     def get_permissions(self):
#         if self.action in ('retrieve', 'list'):
#             return [permissions.AllowAny(), ]
#         return [permissions.IsAdminUser(), ]
#
#     @method_decorator(cache_page(60))  # Кеширование на 1 минуту
#     def list(self, request, *args, **kwargs):
#         return super().list(request, *args, **kwargs)
