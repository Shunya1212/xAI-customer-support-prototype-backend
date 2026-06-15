from django.db import models
from django.contrib.auth import get_user_model
from framework.models import BaseModel, BaseModelQuerySet


User = get_user_model()


class Staff(BaseModel):
    user = models.OneToOneField(User, related_name='staff', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
    
    class Meta:
        ordering = ['-created', '-updated']
        verbose_name = 'Staff'
        verbose_name_plural = 'Staffs'