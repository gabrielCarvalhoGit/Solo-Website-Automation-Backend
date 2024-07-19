import os
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'solo_solutions_api.settings')

app = Celery('solo_solutions_api')
app.config_from_object(f'django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')