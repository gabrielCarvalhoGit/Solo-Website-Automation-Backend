from celery import shared_task
from django.conf import settings
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives


@shared_task
def enviar_email_empresa(empresa, email, link_redefinicao):
    html_content = render_to_string('email/email_empresa_cadastrada.html', {'empresa': empresa, 'link': link_redefinicao})
    text_content = strip_tags(html_content)

    email = EmailMultiAlternatives(
        'Solo Solutions - Mudar senha do usuário',
        text_content,
        settings.EMAIL_HOST_USER,
        [email]
    )
    email.attach_alternative(html_content, 'text/html')
    email.send()