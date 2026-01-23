from celery import Celery
from Backend.controllers.config import config

celery_app = Celery(
    'hospital_management',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0'
)

celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='Asia/Kolkata',
    enable_utc=False,
    
    # Redis connection settings with timeouts
    broker_connection_timeout=2,
    broker_connection_retry_on_startup=False,
    result_backend_transport_options={'socket_timeout': 2},
    
    # Task routing
    task_routes={
        'Backend.controllers.tasks.export_patient_treatments_csv': {'queue': 'exports'},
    },
    
    # Task result expiration (24 hours)
    result_expires=86400,
)

