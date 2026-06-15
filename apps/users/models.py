import uuid
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django_currentuser.db.models import CurrentUserField
from rest_framework.authentication import TokenAuthentication


class BearerTokenAuthentication(TokenAuthentication):
    keyword = 'Bearer'


class BaseUserModelManager(UserManager):
    def actives(self):
        return self.get_queryset().filter(is_active=True)

    def inactives(self):
        return self.get_queryset().filter(is_active=False)


class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, help_text='created date')
    updated = models.DateTimeField(auto_now=True, help_text='updated date')
    created_by = CurrentUserField(related_name='+')
    updated_by = CurrentUserField(related_name='+', on_update=True)
    email = models.EmailField(null=True, blank=True, help_text='email')
    address = models.TextField(null=True, blank=True, help_text='address')
    phone = models.CharField(max_length=32, null=True, blank=True, help_text='phone number')
    profile_image = models.ImageField(upload_to='user', null=True, blank=True, help_text='profile image')
    gender = models.CharField(max_length=150, null=True, blank=True, help_text='gender')
    birth_date = models.DateField(null=True, blank=True, help_text='birth date')
    objects = BaseUserModelManager()

    @staticmethod
    def base_attrs():
        return [
            'created', 'updated', 'created_by',
            'updated_by', 'last_login',
            'user_permissions', 'date_joined', 'is_active'
        ]
    
    @property
    def group_display(self):
        return ', '.join([r.name for r in self.groups.all().order_by('name')])

    @property
    def full_name(self):
        if self.first_name and self.last_name:
            return " ".join(filter(lambda n: n, [self.first_name, self.last_name]))
        return self.username

    def delete(self, *args, **kwargs):
        self.is_active = False
        self.save()

    def __str__(self):
        return self.full_name