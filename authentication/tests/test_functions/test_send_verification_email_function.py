from django.core import mail
from django.template.loader import render_to_string
from django.core.signing import TimestampSigner
from django.test import TestCase
from authentication.functions import send_verification_email
from authentication.models import CustomUser


signer = TimestampSigner()

class SendVerificationEmailTests(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="testuser@example.com",
            email="testuser@example.com",
            password="password123"
        )

    def test_email_is_sent(self):
        send_verification_email(request=None, user=self.user)
        self.assertEqual(len(mail.outbox), 1)

    def test_email_contains_correct_content(self):
        send_verification_email(request=None, user=self.user)
        email = mail.outbox[0]

        self.assertEqual(email.subject, "Confirm your email")
        self.assertEqual(email.to, [self.user.email])
        token = signer.sign(self.user.email)
        expected_url = f"http://127.0.0.1:4200/verification/{token}"
        self.assertIn(expected_url, email.alternatives[0][0]) 

    def test_email_uses_correct_template(self):
        token = signer.sign(self.user.email)
        expected_url = f"http://127.0.0.1:4200/verification/{token}"
        expected_html = render_to_string(
            "verification_email.html", {"user": self.user, "verification_url": expected_url}
        )

        send_verification_email(request=None, user=self.user)

        email_html_content = mail.outbox[0].alternatives[0][0]
        self.assertEqual(email_html_content, expected_html)
