from django.core.mail import send_mail, mail_admins, BadHeaderError
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page 
from django.core.cache import cache 
from rest_framework.views import  APIView
from rest_framework.request import Request
from templated_mail.mail import BaseEmailMessage
from .tasks import notify_customers
import requests
import logging

logger = logging.getLogger(__name__)
logger.info 


class HelloView(APIView):
    @method_decorator(cache_page(5 * 60))
    def get(self, request : Request):
        try:
            logger.info("Calling httpbin...")
            response : requests.Response = requests.get('https://httpbin.org/delay/0')
            logger.info("Received the response...")
            data = response.json()
        except requests.ConnectionError:
            logger.critical("Httpbin is offline")
        return render(request, 'hello.html', {'name': 'Jie'}) 


# @cache_page(5 * 60)
# def say_hello(request):
#     # notify_customers.delay('Hello')
 
#     response : requests.Response = requests.get('https://httpbin.org/delay/2')
#     print(request)
#     data = response.json()
#     return render(request, 'hello.html', {'name': 'Jie'}) 


 