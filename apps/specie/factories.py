import factory
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyChoice
from apps.specie import models


class SpecieFactory(DjangoModelFactory):
    name = factory.Faker('word')
    specific_name = factory.Faker('word')

    class Meta:
        model = models.Specie

class GrowthStateFactory(DjangoModelFactory):
    state = factory.Faker('word')
    sort_no = factory.Faker('pyint', min_value=1, max_value=10)
    note = factory.Faker('word')

    class Meta:
        model = models.GrowthState