from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

class Promo(models.Model):
    # Связь ForeignKey с моделью User, настроена на запрет удаления пользователя, если есть привязанный Promo
    user = models.ForeignKey(User, on_delete=models.RESTRICT, related_name='promo')

    # Поле для загрузки изображения, изображение будет сохранено в папке 'images'
    image = models.ImageField(upload_to='images')

    # Текстовое поле для описания промо, может быть пустым (необязательное поле)
    text = models.TextField(blank=True)

    # Поле для автоматической установки даты и времени создания промо
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'promo'           # Название модели в единственном числе для админки
        verbose_name_plural = 'promo'    # Название модели во множественном числе для админки

    def __str__(self):
        # Возвращает строковое представление объекта Promo, состоящее из имени пользователя и текста промо (первые 25 символов)
        return f'{self.user} - {self.text[:25]}'

# from django.contrib.auth import get_user_model
# from django.db import models
#
# User = get_user_model()
#
#
# class Promo(models.Model):
#     user = models.ForeignKey(User, on_delete=models.RESTRICT,
#                              related_name='promo')
#     image = models.ImageField(upload_to='images')
#     text = models.TextField(blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#
#     class Meta:
#         verbose_name = 'promo'
#         verbose_name_plural = 'promo'
#
#     def __str__(self):
#         return f'{self.user} - {self.text[:25]}'
