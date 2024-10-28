from django.core.mail import send_mail

def send_verification_email(user):
    send_mail(
        "Subject here",
        "Here is the message.",
        "videoflix@martin-inglin.ch",
        [user.username],
        fail_silently=False,
    )