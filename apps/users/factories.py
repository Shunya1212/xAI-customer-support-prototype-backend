import factory
from factory.django import DjangoModelFactory
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group


class UserFactory(DjangoModelFactory):
    username = factory.Faker("user_name")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.Faker("email")
    is_active = True
    password = factory.PostGenerationMethodCall('set_password', 'password123')
    
    @factory.post_generation
    def groups(obj, created, extract, *args, **kwargs):
        if created and extract:
            for group in extract:
                groups, _ = Group.objects.get_or_create(name=group, defaults={})
                groups.user_set.add(obj)
    
    class Meta:
        model = get_user_model()
        skip_postgeneration_save = True


class GroupFactory(DjangoModelFactory):
    name = factory.Faker('job')

    class Meta:
        model = Group