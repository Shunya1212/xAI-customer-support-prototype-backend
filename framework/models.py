import uuid
from django.db import models
from django_currentuser.db.models import CurrentUserField
from django.db.models import signals
from django.dispatch import receiver
from django.utils import timezone
from functools import wraps


class BaseModelQuerySet(models.QuerySet):
    def actives(self) -> models.QuerySet:
        return self.filter(is_active=True)

    def inactives(self) -> models.QuerySet:
        return self.filter(is_active=False)


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(default=timezone.now, editable=False, help_text='Date and time of creation')
    updated = models.DateTimeField(auto_now=True, help_text='Date and time of last update')
    created_by = CurrentUserField(related_name='+')
    updated_by = CurrentUserField(related_name='+', on_update=True)
    is_active = models.BooleanField(default=True, help_text='activate or deactivate this record')
    objects = BaseModelQuerySet.as_manager()

    def delete(self, *args, **kwargs):
        self.is_active = False
        self.save()

    @staticmethod
    def base_attrs():
        return ['created', 'updated', 'created_by', 'updated_by', 'is_active']

    def on_created(self):
        """Override this method for calling functions on created"""
        pass

    def on_updated(self):
        """Override this method for calling functions on updated"""
        pass

    class Meta:
        abstract = True
        ordering = ['-created', '-updated']


def prevent_save_signal_recursion(func):
    """
    Prevent the loop on calling instance.save() inside post_save or pre_save signal
    """
    @wraps(func)
    def no_recursion(*args, **kwargs):
        instance = kwargs.get('instance', None)

        if not instance:
            return

        if hasattr(instance, '_dirty'):
            return

        func(*args, **kwargs)

        try:
            instance._dirty = True
            instance.save()
        finally:
            del instance._dirty

    return no_recursion


@receiver(signals.post_save)
def on_model_saved(sender, instance, created, **kwargs):
    if hasattr(instance, '_dirty'):
        return
    else:
        instance._dirty = True
        instance.save()

    func_name = 'on_created' if created else 'on_updated'
    if hasattr(instance, func_name):
        target_func = getattr(instance, func_name)
        target_func()

    del instance._dirty
