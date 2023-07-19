from rest_framework import serializers
from .models import Category


class CategorySerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Category.

    Аргументы:
    - slug (str, optional): Уникальный идентификатор категории (поле SlugField).
    - name (str): Название категории (поле CharField).
    - parent (Category, optional): Родительская категория (ссылка на себя) (поле ForeignKey).

    Примечание:
    - Сериализатор преобразует объекты модели Category в JSON и обратно.
    """
    slug = serializers.SlugField(required=False)  # Уникальный идентификатор категории (необязательное поле).

    class Meta:
        model = Category
        fields = '__all__'  # Включаем все поля модели Category в сериализацию.



# from rest_framework import serializers
# from .models import Category
#
#
# class CategorySerializer(serializers.ModelSerializer):
#     slug = serializers.SlugField(required=False)
#
#     class Meta:
#         model = Category
#         fields = '__all__'

    # def to_representation(self, instance):
    #     repr = super().to_representation(instance)
    #     children = instance.children.all()
    #     if children:
    #         repr['children'] = CategorySerializer(children, many=True).data
    #     return repr