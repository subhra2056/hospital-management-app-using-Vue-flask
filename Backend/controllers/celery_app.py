from celery import Celery
from Backend.controllers.config import config

celery_app = Celery(
    'hospital_management',
    broker=f'redis://localhost:6379/0',
    backend=f'redis://localhost:6379/0'
)

celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    beat_schedule={
        'daily-appointment-reminders': {
            'task': 'Backend.controllers.tasks.send_daily_reminders',
            'schedule': 60.0,
        },
        'monthly-doctor-reports': {
            'task': 'Backend.controllers.tasks.send_monthly_reports',
            'schedule': 86400.0,
        },
    },
)
