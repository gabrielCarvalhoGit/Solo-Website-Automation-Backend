from ..models import User


class UserRepository:
    def create(self, **kwargs):
        return User.objects.create_user(**kwargs)
    
    def validate_email(self, email):
        return User.objects.filter(email=email).exists()
    
    def generate_password_temp(self):
        return User.objects.make_random_password()
    