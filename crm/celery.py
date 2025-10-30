from __future__ import annotations
import os
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alx_backend_graphql_crm.settings')

app = Celery('alx_backend_graphql_crm')

# Configure using a dictionary from Django settings prefixed with CELERY_
app.config_from_object('django.conf:settings', namespace='CELERY')

# Autodiscover tasks in installed apps (search for tasks.py)
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

# Optional: default config you may want to keep in code
app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',            # keep UTC; Django will convert for display if USE_TZ = True
    enable_utc=True,
    task_track_started=True,
    worker_max_tasks_per_child=100,  # mitigate memory leaks
    worker_prefetch_multiplier=1,    # avoid task starvation where appropriate
)