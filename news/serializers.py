from rest_framework import serializers

from .models import News


class NewsSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели новостей.

    Атрибуты:
    - model (Model): Модель, с которой связан сериализатор.
    - fields (tuple или str): Поля модели, которые будут сериализованы.

    Примечание:
    - В данном случае используется 'serializers.ModelSerializer', который автоматически
      создает сериализатор на основе модели и ее полей, указанных в 'fields'.
      Это позволяет автоматически обрабатывать данные, сохраняя поля и связи модели.
    """
    class Meta:
        model = News
        fields = '__all__'

# from rest_framework import serializers
#
# from .models import News
#
#
# class NewsSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = News
#         fields = '__all__'
