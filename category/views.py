from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import generics, permissions
from . import serializers
from .models import Category


class CategoryCreateListView(generics.ListCreateAPIView):
    """
    Представление для создания и просмотра списка категорий товаров.

    Аргументы:
    - queryset (QuerySet): QuerySet, который определяет набор объектов для представления.
    - serializer_class (Serializer): Сериализатор для преобразования данных категории.
    - permission_classes (tuple): Кортеж с классами разрешений для доступа к представлению.

    Примечание:
    - Представление позволяет создавать новые категории и просматривать список существующих.
    - Разрешено только администраторам (IsAdminUser) создавать новые категории.
    - При просмотре списка категорий применено кеширование на 1 минуту.
    """
    queryset = Category.objects.all()  # QuerySet, содержащий все объекты модели Category.
    serializer_class = serializers.CategorySerializer  # Сериализатор для преобразования данных категории.
    permission_classes = (permissions.IsAdminUser, )  # Только администраторам разрешено создавать категории.

    @method_decorator(cache_page(60))  # Кеширование списка на 1 минуту.
    def list(self, request, *args, **kwargs):
        """
        Метод для получения списка категорий.

        Аргументы:
        - request (Request): Объект запроса.

        Возвращает:
        - Response: Ответ с данными списка категорий.
        """
        return super().list(request, *args, **kwargs)

    def get_permissions(self):
        """
        Возвращает список прав доступа для каждого метода представления.

        Возвращает:
        - tuple: Кортеж с классами разрешений для каждого метода представления.
        """
        if self.request.method == 'GET':
            return permissions.AllowAny(),  # Разрешено всем просматривать список категорий.
        return permissions.IsAdminUser(),  # Только администраторам разрешено создавать новые категории.


class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Представление для просмотра, обновления и удаления отдельной категории товаров.

    Аргументы:
    - queryset (QuerySet): QuerySet, который определяет набор объектов для представления.
    - serializer_class (Serializer): Сериализатор для преобразования данных категории.

    Примечание:
    - Представление позволяет просматривать, обновлять и удалять отдельные категории товаров.
    - Разрешено всем просматривать информацию о категории (GET).
    - Только администраторам разрешено обновлять и удалять категории (PUT, PATCH, DELETE).
    """
    queryset = Category.objects.all()  # QuerySet, содержащий все объекты модели Category.
    serializer_class = serializers.CategorySerializer  # Сериализатор для преобразования данных категории.

    def get_permissions(self):
        """
        Возвращает список прав доступа для каждого метода представления.

        Возвращает:
        - list: Список с классами разрешений для каждого метода представления.
        """
        if self.request.method == 'GET':
            return [permissions.AllowAny(), ]  # Разрешено всем просматривать информацию о категории.
        return [permissions.IsAdminUser(), ]  # Только администраторам разрешено обновлять и удалять категории.

# from django.utils.decorators import method_decorator
# from django.views.decorators.cache import cache_page
# from rest_framework import generics, permissions
# from . import serializers
# from .models import Category
#
#
# class CategoryCreateListView(generics.ListCreateAPIView):
#     queryset = Category.objects.all()
#     serializer_class = serializers.CategorySerializer
#     permission_classes = (permissions.IsAdminUser, )
#
#     @method_decorator(cache_page(60))  # Кеширование на 1 минуту
#     def list(self, request, *args, **kwargs):
#         return super().list(request, *args, **kwargs)
#
#     def get_permissions(self):
#         if self.request.method == 'GET':
#             return permissions.AllowAny(),
#         return permissions.IsAdminUser(),
#
#
# class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Category.objects.all()
#     serializer_class = serializers.CategorySerializer
#
#     def get_permissions(self):
#         if self.request.method == 'GET':
#             return [permissions.AllowAny(), ]
#         return [permissions.IsAdminUser(), ]