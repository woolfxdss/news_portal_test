import os
from celery import Celery

# Установите переменную окружения для настроек Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'news_portal.settings')

app = Celery('news_portal')

# Конфигурация Celery из настроек Django
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автообнаружение задач в приложениях
app.autodiscover_tasks()