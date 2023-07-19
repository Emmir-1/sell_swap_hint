from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from requests import get
from multiprocessing import Pool

from . import serializers
from .models import News
from .tasks import parsing


# Класс для пагинации результатов
class StandartResultPagination(PageNumberPagination):
    """
    Пагинация результатов запроса.

    Атрибуты:
    - page_size (int): Количество элементов на странице (по умолчанию 10).
    - page_query_param (str): Название параметра запроса для указания номера страницы (по умолчанию 'page').
    """
    page_size = 10
    page_query_param = 'page'


# Ваш ViewSet для модели News
class NewsViewSet(ModelViewSet):
    """
    ViewSet для модели News.

    Атрибуты:
    - queryset (QuerySet): Запрос для выборки объектов модели News, упорядоченных по дате создания.
    - pagination_class (class): Класс пагинации для списка результатов.
    - serializer_class (class): Класс сериализатора, используемый для преобразования данных.

    Методы:
    - get_permissions: Возвращает список разрешений в зависимости от типа запроса.
    - list: Переопределенный метод для получения списка объектов News с кешированием на 1 минуту.
    - parse_news: Метод действия API для запуска асинхронной задачи парсинга новостей.
    """
    queryset = News.objects.all().order_by('-created_at')
    pagination_class = StandartResultPagination
    serializer_class = serializers.NewsSerializer

    def get_permissions(self):
        """
        Возвращает список разрешений в зависимости от типа запроса.

        При запросах на получение списка и деталей новостей разрешается доступ всем пользователям (даже анонимным).
        При других запросах требуется права администратора.

        Возвращает:
        - permissions.AllowAny: Разрешение для всех запросов на получение списка и деталей новостей.
        - permissions.IsAdminUser: Разрешение для запросов, требующих права администратора.
        """
        if self.action in ('retrieve', 'list'):
            return [permissions.AllowAny(), ]
        return [permissions.IsAdminUser(), ]

    # Декоратор cache_page для кеширования результатов на 1 минуту
    @method_decorator(cache_page(60))
    def list(self, request, *args, **kwargs):
        """
        Метод для получения списка объектов News с кешированием на 1 минуту.

        Возвращает:
        - super().list(request, *args, **kwargs): Результат выполнения родительского метода list.
        """
        return super().list(request, *args, **kwargs)

    @action(detail=False, methods=['GET'])
    def parse_news(self, request, *args, **kwargs):
        """
        Метод действия API для запуска асинхронной задачи парсинга новостей.

        Запускает задачу парсинга новостей в фоновом режиме с помощью Celery.

        Возвращает:
        - Response('Parse done'): Ответ API с сообщением о запуске парсинга.
        """
        parsing.delay()
        return Response('Parse done')

# from django.utils.decorators import method_decorator
# from django.views.decorators.cache import cache_page
# from rest_framework import permissions
# from rest_framework.decorators import action
# from rest_framework.pagination import PageNumberPagination
# from rest_framework.viewsets import ModelViewSet
# from rest_framework.response import Response
# from requests import get
# # from datetime import datetime
# from multiprocessing import Pool
#
# from . import serializers
# from .models import News
# from .tasks import parsing
#
#
# # Класс для пагинации результатов
# class StandartResultPagination(PageNumberPagination):
#     page_size = 10
#     page_query_param = 'page'
#
#
# # Ваш ViewSet для модели News
# class NewsViewSet(ModelViewSet):
#     queryset = News.objects.all().order_by('-created_at')
#     pagination_class = StandartResultPagination
#     serializer_class = serializers.NewsSerializer
#
#     def get_permissions(self):
#         if self.action in ('retrieve', 'list'):
#             return [permissions.AllowAny(), ]
#         return [permissions.IsAdminUser(), ]
#
#     # Декоратор cache_page для кеширования результатов на 15 минут
#     @method_decorator(cache_page(60))
#     def list(self, request, *args, **kwargs):
#         return super().list(request, *args, **kwargs)
#
#     @action(detail=False, methods=['GET'])
#     def parse_news(self, request, *args, **kwargs):
#         parsing.delay()
#         return Response('Parse done')
