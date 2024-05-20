from django.core.mail import send_mail, mail_admins, BadHeaderError
from django.shortcuts import render
from templated_mail.mail import BaseEmailMessage
from .tasks import notify_customers
import requests

def say_hello(request):
    # notify_customers.delay('Hello')

    requests.get('https://httpbin.org/delay/2 ')
    return render(request, 'hello.html', {'name': 'Mosh'})


 