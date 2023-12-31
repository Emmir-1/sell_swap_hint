from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.response import Response

from .models import OrderItem, Order
from product.models import Product


class OrderItemSerializer(serializers.ModelSerializer):
    """
    Сериализатор для элемента заказа.

    Поля:
    - product_title (ReadOnlyField): Название продукта, только для чтения (source='product.title').
    """
    product_title = serializers.ReadOnlyField(source='product.title')

    class Meta:
        model = OrderItem
        fields = ('product', 'quantity', 'product_title')


class OrderSerializer(serializers.ModelSerializer):
    """
    Сериализатор для заказа.

    Поля:
    - status (CharField): Статус заказа (только для чтения).
    - user (ReadOnlyField): Email пользователя, только для чтения (source='user.email').
    - products (OrderItemSerializer): Сериализатор для элементов заказа (только для записи, множественный).
    """
    status = serializers.CharField(read_only=True)
    user = serializers.ReadOnlyField(source='user.email')
    products = OrderItemSerializer(write_only=True, many=True)

    class Meta:
        model = Order
        fields = '__all__'

    def validate_products(self, products):
        """
        Проверка доступного количества продуктов в заказе.

        Аргументы:
        - products (list): Список элементов заказа.

        Исключения:
        - serializers.ValidationError: Возникает, если количество продуктов в заказе превышает доступное количество.

        Возвращает:
        - list: Отфильтрованный список элементов заказа.
        """
        for product in products:
            product_id = product['product'].id

            product_data = get_object_or_404(Product, id=product_id)

            if product_data.quantity < product['quantity']:
                raise serializers.ValidationError(f'В наличии {product_data.title} {product_data.quantity} шт')
        return products

    def create(self, validated_data):
        """
        Создание заказа и элементов заказа.

        Аргументы:
        - validated_data (dict): Валидированные данные заказа.

        Возвращает:
        - Order: Созданный объект заказа.
        """
        products = validated_data.pop('products')
        user = self.context['request'].user
        total_sum = 0
        for product in products:
            product_id = product['product'].id
            total_sum += product['quantity'] * product['product'].price

            product_data = get_object_or_404(Product, id=product_id)

            product_data.quantity -= product['quantity']
            product_data.save()

        order = Order.objects.create(user=user, total_sum=total_sum, status='open', **validated_data)
        order_item_objects = [
            OrderItem(order=order, product=product['product'], quantity=product['quantity']) for product in products]
        OrderItem.objects.bulk_create(order_item_objects)
        return order

    def to_representation(self, instance):
        """
        Переопределение представления для заказа.

        Аргументы:
        - instance (Order): Экземпляр заказа.

        Возвращает:
        - dict: Представление заказа с сериализованными элементами заказа.
        """
        repr = super().to_representation(instance)
        repr['products'] = OrderItemSerializer(instance.items.all(), many=True).data
        repr.pop('product')
        return repr

# from django.db import transaction
# from django.shortcuts import get_object_or_404
# from rest_framework import serializers
# from rest_framework.response import Response
#
# from .models import OrderItem, Order
# from product.models import Product
#
#
# class OrderItemSerializer(serializers.ModelSerializer):
#     product_title = serializers.ReadOnlyField(source='product.title')
#
#     class Meta:
#         model = OrderItem
#         fields = ('product', 'quantity', 'product_title')
#
#
# class OrderSerializer(serializers.ModelSerializer):
#     status = serializers.CharField(read_only=True)
#     user = serializers.ReadOnlyField(source='user.email')
#     products = OrderItemSerializer(write_only=True, many=True)
#
#     class Meta:
#         model = Order
#         fields = '__all__'
#
#     def validate_products(self, products):
#         for product in products:
#             product_id = product['product'].id
#
#             product_data = get_object_or_404(Product, id=product_id)
#
#             if product_data.quantity < product['quantity']:
#                 raise serializers.ValidationError(f'В наличии {product_data.title} {product_data.quantity} шт')
#         return products
#
#     def create(self, validated_data):
#         products = validated_data.pop('products')
#         user = self.context['request'].user
#         total_sum = 0
#         for product in products:
#             product_id = product['product'].id
#             total_sum += product['quantity'] * product['product'].price
#
#             product_data = get_object_or_404(Product, id=product_id)
#
#             product_data.quantity -= product['quantity']
#             product_data.save()
#
#         order = Order.objects.create(user=user, total_sum=total_sum,
#                                      status='open', **validated_data)
#         order_item_objects = [
#             OrderItem(order=order,
#                       product=product['product'],
#                       quantity=product['quantity']) for product in products]
#         OrderItem.objects.bulk_create(order_item_objects)
#         return order
#
#     def to_representation(self, instance):
#         repr = super().to_representation(instance)
#         repr['products'] = OrderItemSerializer(instance.items.all(),
#                                                many=True).data
#         repr.pop('product')
#         return repr
