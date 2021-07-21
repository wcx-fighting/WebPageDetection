# 将代码里的runyi,改成自己的项目名
import os
from celery import Celery
from celery.utils.log import get_task_logger
from celery.schedules import crontab

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WebpageDetection.settings')

app = Celery('WebpageDetection')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

# 定时任务调度
app.conf.beat_schedule = {
    "every-midnight-check-account-lock": { # 当晚24点整,将所有锁定的账户解锁
        'task': 'get_has_account_lock',
        'schedule': crontab(minute=0, hour=0),
        'args': ()
    }
}
@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')