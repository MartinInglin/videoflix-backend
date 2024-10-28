from django.core.mail import send_mail
from django.template.loader import render_to_string
from videoflix_backend import settings

def send_verification_email(user):
    subject = 'Confirm your email'
    html_message = render_to_string('verification_email.html', {'user': user})
    recipient_list = [user.email]
    send_mail(subject, '', settings.DEFAULT_FROM_EMAIL, recipient_list, html_message=html_message)