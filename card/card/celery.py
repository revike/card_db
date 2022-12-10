import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'card.settings')

app = Celery('card')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'deactivate_card_morning': {
        'task': 'main_app.tasks.deactivate_card',
        'schedule': crontab(hour=5),
    },
    'deactivate_card_dinner': {
        'task': 'main_app.tasks.deactivate_card',
        'schedule': crontab(hour=11),
    },
    'deactivate_card_evening': {
        'task': 'main_app.tasks.deactivate_card',
        'schedule': crontab(hour=17),
    },
    'deactivate_card_night': {
        'task': 'main_app.tasks.deactivate_card',
        'schedule': crontab(hour=21),
    },
}


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request}')
