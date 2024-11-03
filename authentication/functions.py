from django.core.mail import send_mail
from django.template.loader import render_to_string
from videoflix_backend import settings
from django.core.signing import TimestampSigner, SignatureExpired, BadSignature
from django.contrib.auth import get_user_model

signer = TimestampSigner()
User = get_user_model()

def send_verification_email(request, user):
    token = signer.sign(user.email)
    subject = 'Confirm your email'
    verification_url = f'http://127.0.0.1:4200/verification/{token}'
    html_message = render_to_string('verification_email.html', {'user': user, 'verification_url': verification_url})
    recipient_list = [user.email]
    send_mail(subject, '', settings.DEFAULT_FROM_EMAIL, recipient_list, html_message=html_message)
    
def get_user_from_token(token):
    try:
        email = signer.unsign(token)
        user = User.objects.get(email=email)
        return user
    except (BadSignature, SignatureExpired):
        return None
    
def send_reset_password_email(request, email):
    token = signer.sign(email)
    subject = 'Reset Videoflix password'
    reset_password_url = f'http://127.0.0.1:4200/reset-password/{token}'
    html_message = render_to_string('reset_password_email.html', {'reset_password_url': reset_password_url})
    recipient_list = [email]
    send_mail(subject, '', settings.DEFAULT_FROM_EMAIL, recipient_list, html_message=html_message)