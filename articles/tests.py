from django.core.signing import Signer
from django.template.loader import render_to_string
from django.test import TestCase

from articles.utilities import send_activation_notification
from articlesboard.settings import ALLOWED_HOSTS, SITE_NAME
from .models import AdvUser


class EmailMessage(TestCase):
    
    def test_send_activation_notification(self):
        if ALLOWED_HOSTS:
            host = 'http://' + ALLOWED_HOSTS[0]
        else:
            host = 'http://localhost:8000'
        signer = Signer()
        user = AdvUser.objects.get(pk=1)
        context = {'host': host, 'user': user, 'site_name': SITE_NAME, 'sign': signer.sign(user.username)}
        subject = render_to_string('email/test_subject.txt', context=context)
        body = render_to_string('email/test_body.txt', context=context)
        user.email(subject, body)
        