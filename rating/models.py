from django.db import models
from product.models import Product
from django.contrib.auth import get_user_model

User = get_user_model()

# Класс Mark определяет доступные варианты оценок для поля rating
class Mark:
    marks = (
        (1, 'Too bad!'),    # Очень плохо!
        (2, 'Bad!'),        # Плохо
        (3, 'Normal!'),     # Средне
        (4, 'Good!'),       # Хорошо
        (5, 'Excellent!')   # Отлично
    )

class Review(models.Model):
    # Связь ForeignKey с моделью Product, настроена на удаление отзывов при удалении продукта
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')

    # Связь ForeignKey с моделью User, настроена на удаление отзывов при удалении пользователя
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')

    # Поле для хранения оценки отзыва, доступные варианты оценок определены в классе Mark
    rating = models.PositiveSmallIntegerField(choices=Mark.marks)

    # Текстовое поле для описания отзыва, может быть пустым (необязательное поле)
    text = models.TextField(blank=True)

    # Поле для автоматической установки даты и времени создания отзыва
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Уникальное совместное значение для пары (user, product), чтобы пользователь мог оставить только один отзыв на продукт
        unique_together = ['user', 'product']

    def __str__(self):
        # Возвращает строковое представление объекта Review, состоящее из названия продукта, имени пользователя и оценки
        return f'{self.product} -> {self.user} -> {self.rating}'

# from django.db import models
# from product.models import Product
# from django.contrib.auth import get_user_model
#
# User = get_user_model()
#
#
# class Mark:
#     marks = ((1, 'Too bad!'), (2, 'Bad!'), (3, 'Normal!'), (4, 'Good!'),
#              (5, 'Excellent!'))
#
#
# class Review(models.Model):
#     product = models.ForeignKey(Product, on_delete=models.CASCADE,
#                                 related_name='reviews')
#     user = models.ForeignKey(User, on_delete=models.CASCADE,
#                              related_name='reviews')
#     rating = models.PositiveSmallIntegerField(choices=Mark.marks)
#     text = models.TextField(blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#
#     class Meta:
#         unique_together = ['user', 'product']
#
#     def __str__(self):
#         return f'{self.product} -> {self.user} -> {self.rating}'
