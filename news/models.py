from django.db import models

class News(models.Model):
    """
    Модель новостей.

    Поля:
    - title (CharField): Заголовок новости (максимальная длина 255 символов), уникальное значение.
    - image (URLField): URL-адрес изображения, связанного с новостью.
    - text (TextField): Текст новости.
    - created_at (DateTimeField): Дата и время создания новости (автоматически заполняется при создании).

    Метаданные:
    - verbose_name (str): Название модели в единственном числе для административного интерфейса.
    - verbose_name_plural (str): Название модели во множественном числе для административного интерфейса.
    """
    title = models.CharField(max_length=255, unique=True)
    image = models.URLField()
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'news'
        verbose_name_plural = 'news'

    def __str__(self):
        return f'{self.id} {self.title} {self.created_at}'

# from django.db import models
#
#
# class News(models.Model):
#     title = models.CharField(max_length=255, unique=True)
#     image = models.URLField()
#     text = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)
#
#     class Meta:
#         verbose_name = 'news'
#         verbose_name_plural = 'news'
#
#     def __str__(self):
#         return f'{self.id} {self.title} {self.created_at}'
