from account.send_mail import send_notification
from .celery import app


@app.task
def send_notification_task(user_email, order_id, price):
    """
    Асинхронная задача для отправки уведомления пользователю о создании заказа.

    Аргументы:
    - user_email (str): Электронный адрес пользователя, которому отправляется уведомление.
    - order_id (int): Номер созданного заказа.
    - price (float): Полная стоимость заказа.

    Примечание:
    - Задача запускается в фоновом режиме с помощью Celery.
    - Отправляет уведомление о создании заказа на указанный электронный адрес.
    """
    send_notification(user_email, order_id, price)


#---------
# from account.send_mail import send_notification
# # from comment.models import Comment
# from .celery import app
#
#
# @app.task
# def send_notification_task(user_email, order_id, price):
#     send_notification(user_email, order_id, price)
# -----------




# @app.task
# def send_comment_notification_email(comment_id):
#     # Получите комментарий по его ID или каким-либо другим способом
#     comment = Comment.objects.get(id=comment_id)
#
#     # Отправьте уведомление о комментарии по электронной почте
#     subject = 'Уведомление о новом комментарии'
#     message = f'Получен новый комментарий от пользователя {comment.user}: {comment.content}'
#     recipient_list = [comment.user.email]
#     send_mail(subject, message, 'noreply@example.com', recipient_list, fail_silently=False)