from django.template.loader import render_to_string
from django.core.signing import Signer
from articlesboard.settings import ALLOWED_HOSTS, SITE_NAME

signer = Signer()


# Send activation message to user.
def send_activation_notification(user):
    if ALLOWED_HOSTS:
        host = 'http://' + ALLOWED_HOSTS[0]
    else:
        host = 'http://localhost:8000'
        
    context = {'user': user, 'host': host, 'sign': signer.sign(user.username), 'site_name': SITE_NAME}
    subject = render_to_string('email/activation_letter_subject.txt', context)
    body = render_to_string('email/activation_letter_body.txt', context)
    user.email_user(subject, body)
