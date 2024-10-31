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
    verification_url = f'http://127.0.0.1:4200/verification/{user.pk}/{token}'
    html_message = render_to_string('verification_email.html', {'user': user, 'verification_url': verification_url})
    recipient_list = [user.email]
    send_mail(subject, '', settings.DEFAULT_FROM_EMAIL, recipient_list, html_message=html_message)

def verify_user(user_id, token):
    try:

        email = signer.unsign(token, max_age=1)
        user = User.objects.get(id=user_id, email=email)
        user.is_active = True
        user.save()

        return True,

    except (SignatureExpired, BadSignature):
        return False
    
    except User.DoesNotExist:
        return False