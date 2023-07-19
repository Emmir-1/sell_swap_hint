from rest_framework import serializers
from rating.models import Review


class ReviewActionSerializer(serializers.ModelSerializer):
    # Поле только для чтения, которое представляет email пользователя, оставившего отзыв
    user = serializers.ReadOnlyField(source='user.email')

    # Поле только для чтения, которое представляет название продукта, к которому относится отзыв
    product = serializers.ReadOnlyField(source='product.title')

    class Meta:
        model = Review
        fields = '__all__'  # Включаем все поля модели Review в сериализацию


class ReviewSerializer(serializers.ModelSerializer):
    # Поле только для чтения, которое представляет email пользователя, оставившего отзыв
    user = serializers.ReadOnlyField(source='user.email')

    class Meta:
        model = Review
        fields = '__all__'  # Включаем все поля модели Review в сериализацию

    def validate(self, attrs):
        # При валидации проверяем, что пользователь еще не оставил отзыв на данный продукт
        request = self.context['request']
        product = attrs['product']
        user = request.user
        if user.reviews.filter(product=product).exists():
            raise serializers.ValidationError('You already reviewed this product!')
        return attrs


class ReviewUpdateSerializer(serializers.ModelSerializer):
    # Поле только для чтения, которое представляет email пользователя, оставившего отзыв
    user = serializers.ReadOnlyField(source='user.email')

    # Поле только для чтения, которое представляет название продукта, к которому относится отзыв
    product = serializers.ReadOnlyField(source='product.title')

    class Meta:
        model = Review
        fields = '__all__'  # Включаем все поля модели Review в сериализацию

# from rest_framework import serializers
# from rating.models import Review
#
#
# class ReviewActionSerializer(serializers.ModelSerializer):
#     user = serializers.ReadOnlyField(source='user.email')
#     product = serializers.ReadOnlyField(source='product.title')
#
#     class Meta:
#         model = Review
#         fields = '__all__'
#
#
# class ReviewSerializer(serializers.ModelSerializer):
#     user = serializers.ReadOnlyField(source='user.email')
#
#     class Meta:
#         model = Review
#         fields = '__all__'  # rating text
#
#     def validate(self, attrs):
#         request = self.context['request']
#         product = attrs['product']
#         user = request.user
#         if user.reviews.filter(product=product).exists():
#             raise serializers.ValidationError('You already reviewed this product!')
#         return attrs
#
#
# class ReviewUpdateSerializer(serializers.ModelSerializer):
#     user = serializers.ReadOnlyField(source='user.email')
#     product = serializers.ReadOnlyField(source='product.title')
#
#     class Meta:
#         model = Review
#         fields = '__all__'
