from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from order.models import Order
from order.serializers import OrderSerializer


class CreateOrderView(ListCreateAPIView):
    """
    Представление для создания и просмотра заказов.

    Атрибуты:
    - queryset (QuerySet): Запрос для получения списка заказов.
    - serializer_class (OrderSerializer): Сериализатор для заказов.
    - permission_classes (list): Список классов разрешений для доступа к представлению.
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAdminUser | IsAuthenticatedOrReadOnly, ]

    @method_decorator(cache_page(60))  # Кеширование на 1 минуту
    def get(self, request, *args, **kwargs):
        """
        Обработчик HTTP GET-запроса.

        Аргументы:
        - request (Request): Объект запроса.
        - *args: Дополнительные аргументы.
        - **kwargs: Дополнительные именованные аргументы.

        Возвращает:
        - Response: Ответ с данными о заказах или ошибкой в случае отсутствия прав доступа.
        """
        user = request.user
        if user.is_superuser:  # Проверка, является ли пользователь администратором
            orders = Order.objects.all()
        else:
            orders = user.orders.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=200)

# from django.utils.decorators import method_decorator
# from django.views.decorators.cache import cache_page
# from rest_framework.generics import ListCreateAPIView
# from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
# from rest_framework.response import Response
#
# from order.models import Order
# from order.serializers import OrderSerializer
#
#
# class CreateOrderView(ListCreateAPIView):
#     queryset = Order.objects.all()
#     serializer_class = OrderSerializer
#     permission_classes = [IsAdminUser | IsAuthenticatedOrReadOnly, ]
#
#     @method_decorator(cache_page(60))
#     def get(self, request, *args, **kwargs):
#         user = request.user
#         if user.is_superuser:  # Проверка, является ли пользователь администратором
#             orders = Order.objects.all()
#         else:
#             orders = user.orders.all()
#         serializer = OrderSerializer(orders, many=True)
#         return Response(serializer.data, status=200)