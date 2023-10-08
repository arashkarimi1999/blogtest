from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from django.conf import settings


def SendMail():
    subject = 'test smtp'
    message = '''
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = 'arashkarimi1999@gmail.com'
EMAIL_HOST_PASSWORD = 'weflfydlvnqirklu'
'''
    email_from = settings.EMAIL_HOST_USER
    recipient_list = ['karimiwork99@gmail.com', 'hosseinhj1380@gmail.com']
    print(subject, message, email_from, recipient_list)
    send_mail( subject, message, email_from, recipient_list )