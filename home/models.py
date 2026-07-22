from django.db import models
from .managers import CustomBaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.conf import settings
import uuid
# Create your models here.



class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('Email Address'), unique=True)
    first_name = models.CharField(max_length=225, default='')
    last_name = models.CharField(max_length=225, default='')
    phone_number = models.CharField(max_length=20, null=True)
    deactivated = models.BooleanField(default=False)
    location = models.CharField(max_length=500, default='')
    profile_image = models.ImageField(upload_to='image/', null=True)
    bio = models.TextField(null=True, default='')
    professional_summary = models.TextField(max_length=1000, default='')
    professional_headlines = models.TextField(default='')
    about_me = models.TextField(default='')
    user_tech_stack = models.TextField(default='')
    github_url = models.URLField(null=True, default='')
    linkedin_url = models.URLField(null=True, default='')
    is_active = models.BooleanField(default=True)
    tech_field = models.CharField(max_length=500, default='')
    user_id = models.UUIDField(default=uuid.uuid4)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomBaseUserManager()

    def __str__(self):
        return self.email
    
class PortfolioView(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    ip_address = models.GenericIPAddressField()
    viewed_at = models.DateTimeField(auto_now_add=True)

class ProjectStack(models.Model):
    STATUS = (
        ('Draft', 'Draft'),
        ('Published', 'Published')
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    project_title = models.CharField(max_length=500, null=True)
    project_description = models.TextField(null=True)
    impact_metrics = models.CharField(max_length=225, null=True)
    repository_url = models.URLField(null=True)
    project_tech_stack = models.TextField(default='')
    live_demo_url = models.URLField(null=True)
    cover_image = models.ImageField(upload_to='image/', null=True)
    status = models.CharField(max_length=225, choices=STATUS, null=True)
    project_views = models.IntegerField(default=0)
    uploaded_on = models.DateTimeField(auto_now_add=True)



class UserExperience(models.Model):
    STATUS = (
        ('Draft', 'Draft'),
        ('Published', 'Published')
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=225)
    job_title = models.CharField(max_length=225)
    employment_type = models.CharField(max_length=225)
    location = models.CharField(max_length=225)
    start_time = models.DateField()
    end_time = models.DateField(null=True)
    short_description = models.TextField()
    key_responsibilities = models.TextField(max_length=1000, null=True)
    company_website = models.URLField()
    tech_stack = models.TextField(max_length=1000, default='', null=True)
    status = models.CharField(max_length=225, choices=STATUS, null=True)
    working_currently = models.BooleanField(default=False)
    uploaded_on = models.DateTimeField(auto_now_add=True)



class ClientContactForm(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=225)
    email = models.CharField(max_length=225)
    subject = models.CharField(max_length=500)
    message = models.TextField()
    viewed = models.BooleanField(default=False)
    sent_on = models.DateTimeField(auto_now_add=True)