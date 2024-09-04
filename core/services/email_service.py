from django.core.mail import send_mail
from rest_framework.exceptions import ValidationError


class EmailService:
    def send_reset_password_email(self, token, email):
        reset_link = f'http://localhost:3000/reset-password?token={token}'

        subject = 'Redefinição de Senha'
        message = f'Clique no link para redefinir sua senha: {reset_link}'
        recipient_list = [email]

        self.send_email(subject, message, recipient_list)

    @staticmethod
    def send_email(subject, message, recipient_list, from_email='no-reply@myapp.com'):
        send_mail(
            subject,
            message,
            from_email,
            recipient_list,
            fail_silently=False
        )