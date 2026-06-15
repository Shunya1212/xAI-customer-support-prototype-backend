import factory
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyChoice
from apps.breeding import models
from apps.animal.factories import AnimalFactory


class BreedingPairFactory(DjangoModelFactory):
    code = factory.Faker('word')
    male = factory.SubFactory(AnimalFactory, sex='male')
    female = factory.SubFactory(AnimalFactory, sex='female')
    paring_date = factory.Faker('date')
    status = FuzzyChoice(models.BreedingPair.BreedingResult.choices)
    note = factory.Faker('paragraph', nb_sentences=3)

    class Meta:
        model = models.BreedingPair


class EggBatchFactory(DjangoModelFactory):
    code = factory.Faker('word')
    breeding_pair = factory.SubFactory(BreedingPairFactory)
    laid_date = factory.Faker('date')
    laid_egg_amount = factory.Faker('pyint', min_value=10, max_value=30)
    hatched_egg_amount = factory.Faker('pyint', min_value=1, max_value=10)
    note = factory.Faker('paragraph', nb_sentences=3)

    class Meta:
        model = models.EggBatch