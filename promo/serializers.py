from rest_framework import serializers

from promo.models import Promo

class PromoSerializer(serializers.ModelSerializer):
    # Создаём поле только для чтения (ReadOnlyField), которое ссылается на id пользователя
    # Это нужно, чтобы при сериализации Promo объекта, пользователь был представлен только своим id
    user = serializers.ReadOnlyField(source='user.id')

    class Meta:
        model = Promo  # Связываем сериализатор с моделью Promo
        fields = '__all__'  # Включаем все поля модели Promo в сериализацию

# from rest_framework import serializers
#
# from promo.models import Promo
#
#
# class PromoSerializer(serializers.ModelSerializer):
#     user = serializers.ReadOnlyField(source='user.id')
#
#     class Meta:
#         model = Promo
#         fields = '__all__'
