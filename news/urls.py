from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

# Создаем экземпляр DefaultRouter для автоматической генерации URL-маршрутов
# на основе ViewSet'ов.
router = DefaultRouter()

# Регистрируем ViewSet 'NewsViewSet' с префиксом 'news' в маршрутизаторе.
# Это автоматически создаст URL-маршруты для операций CRUD (create, retrieve, update, delete)
# для модели News.
router.register('news', views.NewsViewSet)

# Определение маршрутов URL для приложения.
urlpatterns = [
    # Подключаем автоматически сгенерированные URL-маршруты из маршрутизатора.
    path('', include(router.urls)),
]

# from django.urls import include, path
# from rest_framework.routers import DefaultRouter
#
# from . import views
#
# router = DefaultRouter()
# router.register('news', views.NewsViewSet)
#
# urlpatterns = [
#     path('', include(router.urls)),
#     ]