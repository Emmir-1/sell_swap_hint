from config.celery import app

# Импортируем функцию main из команды parse_news.
from news.management.commands.parse_news import main


@app.task
def parsing():
    """
    Асинхронная задача для запуска парсинга новостей.

    Примечание:
    - Задача запускается в фоновом режиме с помощью Celery.
    - Выполняет функцию main из команды parse_news для выполнения парсинга новостей.
    """
    main()

# from config.celery import app
#
#
# from news.management.commands.parse_news import main
#
#
# @app.task
# def parsing():
#     main()
