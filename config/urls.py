from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Создаем экземпляр SchemaView для генерации документации API.
schema_view = get_schema_view(
   openapi.Info(
      title="Sell Swap",
      default_version='v1',
      description="Test restful API",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

# Определение маршрутов URL для приложения.
urlpatterns = [
    # Административный интерфейс Django.
    path('admin/', admin.site.urls),

    # Представления для документации API с использованием drf-yasg.
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    # Подключение URL-маршрутов из других приложений.
    path('api/v1/accounts/', include('account.urls')),
    path('api/v1/categories/', include('category.urls')),
    path('api/v1/', include('product.urls')),
    path('api/v1/orders/', include('order.urls')),
    path('api/v1/ratings/', include('rating.urls')),
    path('api/v1/', include('promo.urls')),
    path('api/v1/', include('tracking.urls')),
    path('api/v1/', include('news.urls')),
]

# Добавляем маршруты для обслуживания медиа-файлов в режиме разработки.
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# from django.contrib import admin
# from django.conf import settings
# from django.conf.urls.static import static
# from django.urls import path, include, re_path
# from rest_framework import permissions
# from drf_yasg.views import get_schema_view
# from drf_yasg import openapi
#
#
# schema_view = get_schema_view(
#    openapi.Info(
#       title="Sell Swap",
#       default_version='v1',
#       description="Test restful API",
#       terms_of_service="https://www.google.com/policies/terms/",
#       contact=openapi.Contact(email="contact@snippets.local"),
#       license=openapi.License(name="BSD License"),
#    ),
#    public=True,
#    permission_classes=[permissions.AllowAny],
# )
#
#
# urlpatterns = [
#     path('admin/', admin.site.urls),
#     re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
#     path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
#     re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
#     path('api/v1/accounts/', include('account.urls')),
#     path('api/v1/categories/', include('category.urls')),
#     path('api/v1/', include('product.urls')),
#     path('api/v1/orders/', include('order.urls')),
#     path('api/v1/ratings/', include('rating.urls')),
#     path('api/v1/', include('promo.urls')),
#     path('api/v1/', include('tracking.urls')),
#     path('api/v1/', include('news.urls')),
# ]
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
