from django.core.mail import send_mail
from django.template.loader import render_to_string
from videoflix_backend import settings

def send_verification_email(request, user, token):
    subject = 'Confirm your email'
    #verification_url = request.build_absolute_uri(f'/verify-email/{user.pk}/{token}/')
    verification_url = f'http://127.0.0.1:4200/verification/{user.pk}/{token}'
    html_message = render_to_string('verification_email.html', {'user': user, 'verification_url': verification_url})
    recipient_list = [user.email]
    send_mail(subject, '', settings.DEFAULT_FROM_EMAIL, recipient_list, html_message=html_message)