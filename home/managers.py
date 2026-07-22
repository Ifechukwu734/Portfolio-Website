from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _



class CustomBaseUserManager(BaseUserManager):

    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_('Email is required'))
        email = self.normalize_email(email=email)
        user = self.model(email, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('superuser must have is_superuser=True'))
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('superuser must have is_staff=True'))
        
        return self.create_user(email, password, **extra_fields)