from random import randint
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Avg, Count
from category.models import Category
from ckeditor.fields import RichTextField
from decimal import Decimal

User = get_user_model()


class Product(models.Model):
    """
    Модель для продуктов.

    Атрибуты:
    - owner (ForeignKey): Владелец продукта.
    - title (CharField): Заголовок продукта.
    - description (RichTextField): Описание продукта (использует ckeditor).
    - category (ForeignKey): Категория, к которой относится продукт.
    - price (DecimalField): Цена продукта.
    - quantity (PositiveSmallIntegerField): Количество доступных продуктов.
    - preview (ImageField): Превью изображение продукта.
    - created_at (DateTimeField): Дата создания продукта.
    - updated_at (DateTimeField): Дата обновления продукта.
    """
    owner = models.ForeignKey(User, on_delete=models.RESTRICT, related_name='products')
    title = models.CharField(max_length=150)
    description = RichTextField()
    category = models.ForeignKey(Category, related_name='products', on_delete=models.RESTRICT)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    quantity = models.PositiveSmallIntegerField(default=0)
    preview = models.ImageField(upload_to='images/', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class ProductImage(models.Model):
    """
    Модель для изображений продуктов.

    Атрибуты:
    - product (ForeignKey): Продукт, к которому относится изображение.
    - image (ImageField): Изображение продукта.
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='images', blank=True, null=True)

    def generate_name(self):
        return 'image' + str(randint(100000, 999999))

    def save(self, *args, **kwargs):
        self.title = self.generate_name()
        return super(ProductImage, self).save(*args, **kwargs)


class Likes(models.Model):
    """
    Модель для лайков продуктов.

    Атрибуты:
    - user (ForeignKey): Пользователь, который поставил лайк.
    - product (ForeignKey): Продукт, к которому относится лайк.
    - is_liked (BooleanField): Флаг, указывающий наличие лайка (True) или его отсутствие (False).
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='likes')
    is_liked = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.product} -> {self.user} -> {self.is_liked}'

    class Meta:
        verbose_name = 'like'
        verbose_name_plural = 'likes'


class Favorite(models.Model):
    """
    Модель для избранных продуктов пользователей.

    Атрибуты:
    - user (ForeignKey): Пользователь, который добавил продукт в избранное.
    - product (ForeignKey): Продукт, который добавлен в избранное.
    - favorite (BooleanField): Флаг, указывающий, добавлен продукт в избранное (True) или нет (False).
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='favorites')
    favorite = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.product} -> {self.user} -> {self.favorite}'

# from random import randint
#
# from django.contrib.auth import get_user_model
# from django.db import models
# from django.db.models import Avg, Count
#
# from category.models import Category
# from ckeditor.fields import RichTextField
# from decimal import Decimal
#
# User = get_user_model()
#
#
# class Product(models.Model):
#     owner = models.ForeignKey(User, on_delete=models.RESTRICT,
#                               related_name='products')
#     title = models.CharField(max_length=150)
#     description = RichTextField()
#     category = models.ForeignKey(Category, related_name='products',
#                                  on_delete=models.RESTRICT)
#     price = models.DecimalField(max_digits=12, decimal_places=2)
#     quantity = models.PositiveSmallIntegerField(default=0)
#     preview = models.ImageField(upload_to='images/', null=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#     def __str__(self):
#         return self.title
#
#
# class ProductImage(models.Model):
#     product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
#     image = models.ImageField(upload_to='images', blank=True, null=True)
#
#     def generate_name(self):
#         return 'image' + str(randint(100000, 999999))
#
#     def save(self, *args, **kwargs):
#         self.title = self.generate_name()
#         return super(ProductImage, self).save(*args, **kwargs)
#
#
# class Likes(models.Model):
#     user = models.ForeignKey(User,
#                              on_delete=models.CASCADE,
#                              related_name='likes')
#     product = models.ForeignKey(Product,
#                                 on_delete=models.CASCADE, related_name='likes')
#
#     is_liked = models.BooleanField(default=False)
#
#     def __str__(self):
#         return f'{self.product} -> {self.user} -> {self.is_liked}'
#
#     class Meta:
#         verbose_name = 'like'
#         verbose_name_plural = 'likes'
#
#
# class Favorite(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
#     product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='favorites')
#     favorite = models.BooleanField(default=False)
#
#     def __str__(self):
#         return f'{self.product} -> {self.user} -> {self.favorite}'
