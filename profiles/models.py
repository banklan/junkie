from django.conf import settings
from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth import get_user_model
from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _

from django_resized import ResizedImageField

# User = get_user_model()


class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email must be entered.")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff set to True')

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser set to True')

        return self._create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    GENDER = (
        ('M', 'Male'),
        ('F', 'Female')
    )
    username = None
    email = models.EmailField(_('email address'), unique=True)
    gender = models.CharField(choices=GENDER, max_length=2, default='M')
    phone_no = models.CharField(max_length=15, null=True, blank=True)
    location = models.CharField(max_length=200, null=True, blank=True)
    picture = ResizedImageField(size=[320, 250], quality=85, upload_to="profiles", blank=True, null=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    class Meta:
        verbose_name =('user')
        verbose_name_plural = ('users')
        # abstract = True

    def get_gender(self):
        if self.gender == 'F':
            return 'Female'
        return 'Male'

    def get_fullname(self):
        return self.first_name + ' ' + self.last_name

    def get_picture(self):
        if self.picture:
            return self.picture.url
        return settings.MEDIA_URL + 'profiles/no_image.jpg'
