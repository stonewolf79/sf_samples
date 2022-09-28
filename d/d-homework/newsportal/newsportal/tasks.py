from celery import shared_task
import time

@shared_task
def hello():
    time.sleep(10)
    print("test celery task")