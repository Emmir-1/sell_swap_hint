from django.db import models

class PageView(models.Model):
    # Поле для хранения даты и времени просмотра страницы, устанавливается автоматически при создании объекта
    timestamp = models.DateTimeField(auto_now_add=True)

    # Поле для хранения названия страницы, максимальная длина 255 символов
    page = models.CharField(max_length=255)

    # Поле для хранения IP-адреса, используется для определения, с какого IP была совершена страница
    ip_address = models.GenericIPAddressField()

    def __str__(self):
        # Возвращает строковое представление объекта PageView, состоящее из названия страницы и времени просмотра
        return f'{self.page} - {self.timestamp}'

# from django.db import models
#
#
# class PageView(models.Model):
#     timestamp = models.DateTimeField(auto_now_add=True)
#     page = models.CharField(max_length=255)
#     ip_address = models.GenericIPAddressField()
#
#     def __str__(self):
#         return f'{self.page} - {self.timestamp}'
