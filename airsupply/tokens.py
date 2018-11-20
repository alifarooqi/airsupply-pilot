from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six
from .models import User
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp) +
            six.text_type(user.is_active)
        )


account_activation_token = TokenGenerator()


def send_activation_link(request, id):
    current_site = get_current_site(request)
    user = User.objects.get(pk=id)
    message = render_to_string('acc_active_email.html', {
        'user': user, 'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
        'token': account_activation_token.make_token(user),
    })
    # Sending activation link in terminal
    # user.email_user(subject, message)
    mail_subject = 'Activate your Air Supply Pilot account.'
    to_email = user.email
    email = EmailMessage(mail_subject, message, to=[to_email])
    email.send()
