from rest_framework import serializers
from .models import PageView

class PageViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = PageView
        fields = '__all__'  # Включаем все поля модели PageView в сериализацию

# from rest_framework import serializers
# from .models import PageView
#
#
# class PageViewSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = PageView
#         fields = '__all__'
