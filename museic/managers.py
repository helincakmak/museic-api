# myapp/managers.py
from django.contrib.auth.models import BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        """Normal bir kullanıcı oluşturmak için bu fonksiyonu kullanın."""
        if not email:
            raise ValueError('Kullanıcı e-posta adresine sahip olmalı.')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        """Superuser oluşturmak için bu fonksiyonu kullanın."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, username, password, **extra_fields)
