from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet

from .models import Review
from .serializers import ReviewSerializer

class RatingViewSet(ModelViewSet):
    # Запрос всех объектов модели Review
    queryset = Review.objects.all()

    # Указываем, какой сериализатор использовать для преобразования объектов в JSON и обратно
    serializer_class = ReviewSerializer

    def perform_create(self, serializer):
        # Устанавливаем текущего аутентифицированного пользователя в качестве автора отзыва
        serializer.save(user=self.request.user)

    def get_permissions(self):
        # Возвращаем разрешения в зависимости от типа действия (action)
        if self.action in ('update', 'partial_update', 'destroy'):
            return [permissions.IsAdminUser(), ]  # Только администраторам разрешено изменение и удаление отзывов
        return [permissions.IsAuthenticatedOrReadOnly(), ]  # Для других действий разрешено аутентифицированным пользователям, остальным только чтение # Аутентифицированным пользователям разрешено создание и просмотр отзывов

# from rest_framework import permissions
# from rest_framework.viewsets import ModelViewSet
#
# from .models import Review
# from .serializers import ReviewSerializer
#
#
# class RatingViewSet(ModelViewSet):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer
#
#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)
#
#     def get_permissions(self):
#         if self.action in ('update', 'partial_update', 'destroy'):
#             return [permissions.IsAdminUser(), ]
#         return [permissions.IsAuthenticatedOrReadOnly(), ]
