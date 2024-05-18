from time import sleep
# from storefront.celery import celery
from celery import shared_task

@shared_task
def notify_customers(message):
    print('Sending 10k Emails...')
    print(message) 
    sleep(6)
    print("Emails were sent successfully")