from django.urls import path, include
from . import views
from rest_framework.routers import SimpleRouter
from account.views import UserViewSet
from .views import ChangePasswordView

# Создаем экземпляр SimpleRouter для упрощенного определения URL-маршрутов для API-представлений.
router = SimpleRouter()
router.register('', UserViewSet)  # Регистрируем представление UserViewSet для маршрута '' (пустой).

urlpatterns = [
    # Маршрут для представления LoginView, которое обрабатывает авторизацию пользователей.
    path('login/', views.LoginView.as_view()),
    # Маршрут для представления RefreshView, которое обрабатывает обновление токена доступа.
    path('refresh/', views.RefreshView.as_view()),
    # Включаем URL-маршруты, определенные с помощью SimpleRouter, добавляя их в основные URL-паттерны.
    path('', include(router.urls)),
    # Маршрут для представления ChangePasswordView, которое обрабатывает изменение пароля пользователей.
    path('change-password/', views.ChangePasswordView.as_view()),
    # Маршруты для сброса пароля с использованием пакета django_rest_passwordreset.
    path('password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
]

# from django.urls import path, include
# from . import views
# from rest_framework.routers import SimpleRouter
# from account.views import UserViewSet
# from .views import ChangePasswordView
#
# router = SimpleRouter()
# router.register('', UserViewSet)
#
# urlpatterns = [
#     path('login/', views.LoginView.as_view()),
#     path('refresh/', views.RefreshView.as_view()),
#     path('', include(router.urls)),
#     path('change-password/', views.ChangePasswordView.as_view()),
#     path('password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
# ]

