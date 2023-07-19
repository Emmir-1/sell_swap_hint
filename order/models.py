from django.db import models
from django.contrib.auth import get_user_model
from product.models import Product
from django.db.models.signals import post_save
from django.dispatch import receiver

# from account.send_mail import send_notification
from config.tasks import send_notification_task

User = get_user_model()

STATUS_CHOICES = (
    ('open', 'Открыт'),
    ('in_process', 'В обработке'),
    ('closed', 'Закрыт')
)

class OrderItem(models.Model):
    """
    Модель элемента заказа.

    Атрибуты:
    - order (ForeignKey): Ссылка на заказ, к которому относится данный элемент.
    - product (ForeignKey): Ссылка на продукт, связанный с элементом заказа.
    - quantity (PositiveSmallIntegerField): Количество продуктов в данном элементе заказа (по умолчанию 1).
    """
    order = models.ForeignKey('Order', related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=1)

class Order(models.Model):
    """
    Модель заказа.

    Атрибуты:
    - user (ForeignKey): Ссылка на пользователя, который оформил заказ.
    - product (ManyToManyField): Ссылка на продукты, связанные с заказом через модель OrderItem.
    - address (CharField): Адрес доставки заказа.
    - number (CharField): Уникальный номер заказа (максимальная длина 50 символов).
    - status (CharField): Статус заказа (выбор из предопределенных вариантов STATUS_CHOICES).
    - total_sum (DecimalField): Общая сумма заказа с точностью до двух знаков после запятой (максимальное количество цифр 9).
    - created_at (DateTimeField): Дата и время создания заказа (автоматически устанавливается при создании).
    - updated_at (DateTimeField): Дата и время последнего обновления заказа (автоматически обновляется при изменении).
    """
    user = models.ForeignKey(User, related_name='orders', on_delete=models.CASCADE)
    product = models.ManyToManyField(Product, through=OrderItem)
    address = models.CharField(max_length=255)
    number = models.CharField(max_length=50)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    total_sum = models.DecimalField(max_digits=9, decimal_places=2, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.id} -> {self.user}'

@receiver(post_save, sender=Order)
def order_post_save(sender, instance, *args, **kwargs):
    """
    Обработчик сигнала post_save для модели Order.

    Отправляет асинхронное задание для отправки уведомления о создании заказа пользователю.

    Аргументы:
    - sender: Класс модели, которая инициировала сигнал (в данном случае Order).
    - instance: Экземпляр модели Order, который был сохранен.
    """
    send_notification_task.delay(instance.user.email, instance.id, instance.total_sum)

# from django.db import models
# from django.contrib.auth import get_user_model
# from product.models import Product
# from django.db.models.signals import post_save
# from django.dispatch import receiver
#
# # from account.send_mail import send_notification
# from config.tasks import send_notification_task
#
# User = get_user_model()
#
# STATUS_CHOICES = (
#     ('open', 'Открыт'),
#     ('in_proccess', 'В обработке'),
#     ('closed', 'Закрыт')
# )
#
#
# class OrderItem(models.Model):
#     order = models.ForeignKey('Order', related_name='items',
#                               on_delete=models.CASCADE)
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     quantity = models.PositiveSmallIntegerField(default=1)
#
#
# class Order(models.Model):
#     user = models.ForeignKey(User, related_name='orders',
#                              on_delete=models.CASCADE)
#     product = models.ManyToManyField(Product, through=OrderItem)
#     address = models.CharField(max_length=255)
#     number = models.CharField(max_length=50)
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES)
#     total_sum = models.DecimalField(max_digits=9, decimal_places=2,
#                                     blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#     def __str__(self):
#         return f'{self.id} -> {self.user}'
#
#
# @receiver(post_save, sender=Order)
# def order_post_save(sender, instance, *args, **kwargs):
#     send_notification_task.delay(
#         instance.user.email, instance.id, instance.total_sum
#     )
