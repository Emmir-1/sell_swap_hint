from django.core.mail import send_mail

HOST = 'localhost:3000'


def send_confirmation_email(user, code):
    """
    Отправляет письмо для подтверждения аккаунта с уникальным кодом активации.

    Аргументы:
    - user (str): Email пользователя, на которого отправляется письмо.
    - code (str): Уникальный код активации, который будет добавлен в ссылку подтверждения.

    Примечание:
    - Письмо содержит ссылку на страницу активации аккаунта с переданным кодом.
    """
    link = f'http://{HOST}/api/v1/accounts/activate/{code}/'
    send_mail(
        'Здравствуйте, активируйте ваш аккаунт!',
        f'Чтобы активировать ваш аккаунт нужно перейти по ссылке ниже:'
        f'\n{link}'
        f'\nСсылка работает один раз!',
        'kochemarov@gmail.com',  # Отправитель письма (ваш email).
        [user],  # Получатель письма (email пользователя).
        fail_silently=False,
    )


def send_notification(user_email, order_id, price):
    """
    Отправляет уведомление пользователю о созданном заказе.

    Аргументы:
    - user_email (str): Email пользователя, которому отправляется уведомление.
    - order_id (int): Номер созданного заказа.
    - price (float): Полная стоимость заказа.

    Примечание:
    - Письмо содержит информацию о заказе, его номере и стоимости.
    """
    send_mail(
        'Уведомление о создании заказа!',
        f'''Вы создали заказ №{order_id}, ожидайте звонка!
            Полная стоимость вашего заказа: {price}.
            Спасибо за то что выбрали нас!''',
        'from@example.com',  # Отправитель письма (замените на ваш email или название).
        [user_email],  # Получатель письма (email пользователя).
        fail_silently=False
    )


# from django.core.mail import send_mail
#
# HOST = 'localhost:3000'
#
#
# def send_confirmation_email(user, code):
#     link = f'http://{HOST}/api/v1/accounts/activate/{code}/'
#     send_mail(
#         'Здравствуйте, активируйте ваш аккаунт!',
#         f'Чтобы активировать ваш аккаунт нужно перейти по ссылке ниже:'
#         f'\n{link}'
#         f'\nСсылка работает один раз!',
#         'kochemarov@gmail.com',
#         [user],
#         fail_silently=False,
#     )
#
#
# def send_notification(user_email, order_id, price):
#     send_mail(
#         'Уведомление о создании заказа!',
#         f'''Вы создали заказ №{order_id}, ожидайте звонка!
#             Полная стоимость вашего заказа: {price}.
#             Спасибо за то что выбрали нас!''',
#         'from@exmple.com',
#         [user_email],
#         fail_silently=False
#     )
