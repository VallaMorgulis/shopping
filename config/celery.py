# import os
# from celery import Celery
#
# # Установка переменной окружения, содержащей имя Django-проекта
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project.settings')
#
# # Создание экземпляра Celery
# app = Celery('config')
#
# # Загрузка настроек Celery из файла Django settings.py
# app.config_from_object('django.conf:settings', namespace='CELERY')
#
# # Обнаружение и регистрация задач в приложениях Django
# app.autodiscover_tasks()


import os
from celery import Celery


os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE', 'config.settings'
)

app = Celery('config')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()