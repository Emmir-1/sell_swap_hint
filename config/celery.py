import os
from celery import Celery


# Устанавливаем переменную окружения для настройки Django.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Создаем экземпляр Celery и называем его 'app'.
app = Celery('config')

# Конфигурируем Celery, используя настройки из объекта 'settings' в Django.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматически обнаруживаем и регистрируем задачи в приложениях Django.
app.autodiscover_tasks()

# Опциональные настройки для соединения с брокером очередей (например, RabbitMQ или Redis).
broker_connection_retry = True  # Включаем повторное подключение к брокеру в случае сбоя связи.
broker_connection_retry_on_startup = True  # Повторное подключение при запуске приложения.

# import os
# from celery import Celery
#
#
# os.environ.setdefault(
#     'DJANGO_SETTINGS_MODULE', 'config.settings'
# )
#
# app = Celery('config')
# app.config_from_object('django.conf:settings', namespace='CELERY')
# app.autodiscover_tasks()
# broker_connection_retry = True
# broker_connection_retry_on_startup = True