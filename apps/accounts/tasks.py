from celery import shared_task
from django.conf import settings
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives


@shared_task
def send_email_user(user, link):
    html_content = render_to_string('email/email_reset_user.html', {'user': user, 'link': link})
    text_content = strip_tags(html_content)

    email = EmailMultiAlternatives(
        'Solo Solutions - Mudar senha do usuário',
        text_content,
        settings.EMAIL_HOST_USER,
        [user]
    )
    email.attach_alternative(html_content, 'text/html')
    email.send()