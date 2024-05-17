from django.core.mail import send_mail, mail_admins, BadHeaderError
from django.shortcuts import render


def say_hello(request):
    try:
        send_mail('subject', 'message', 'from@moshy.com', ['bob@hotmail.com'])
    except BadHeaderError:
        pass
    return render(request, 'hello.html', {'name': 'Mosh'})
