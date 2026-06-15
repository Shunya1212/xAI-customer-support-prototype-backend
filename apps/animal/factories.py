import factory
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyChoice
from apps.animal import models
from apps.specie.factories import SpecieFactory


class AnimalFactory(DjangoModelFactory):
    code = factory.Faker('word')
    specie = factory.SubFactory(SpecieFactory)
    sex = FuzzyChoice(models.Animal.Sex.choices)
    hatch_date = factory.Faker('date')
    acquisition_date = factory.Faker('date')
    origin = FuzzyChoice(models.Animal.Origin.choices)
    genetic_value_note = factory.Faker('paragraph', nb_sentences=3)
    status = FuzzyChoice(models.Animal.Status.choices)
    is_assist_feed_needed = factory.Faker('boolean', chance_of_getting_true=20)

    class Meta:
        model = models.Animal


class SizeLogTransactionFactory(DjangoModelFactory):
    animal = factory.SubFactory(AnimalFactory)
    weight = factory.Faker('pydecimal', right_digits=2, positive=True, max_value=3000)
    length = factory.Faker('pydecimal', right_digits=2, positive=True, max_value=3000)
    waist = factory.Faker('pydecimal', right_digits=2, positive=True, max_value=3000)
    date = factory.Faker('date')
    note = factory.Faker('paragraph', nb_sentences=3)

    class Meta:
        model = models.SizeLogTransaction


class FeedingLogTransactionFactory(DjangoModelFactory):
    animal = factory.Faker(AnimalFactory)
    food = factory.SubFactory('apps.feeding.factories.FoodFactory')
    amount = factory.Faker('pyint', min_value=1, max_value=10)
    date = factory.Faker('date')
    feeding_type = FuzzyChoice(models.FeedingLogTransaction.FeedingType.choices)
    note = factory.Faker('paragraph', nb_sentences=3)

    class Meta:
        model = models.FeedingLogTransaction


class FeedingResultLogTransactionFactory(DjangoModelFactory):
    transaction = factory.SubFactory(FeedingLogTransactionFactory)
    date = factory.Faker('date')
    result = FuzzyChoice(models.FeedingResultLogTransaction.Result.choices)
    note = factory.Faker('paragraph', nb_sentences=3)

    class Meta:
        model = models.FeedingResultLogTransaction


class DeadLogTransactionFactory(DjangoModelFactory):
    animal = factory.SubFactory(AnimalFactory)
    date = factory.Faker('date')
    cause = FuzzyChoice(models.DeadLogTransaction.Cause.choices)
    note = factory.Faker('paragraph', nb_sentences=3)

    class Meta:
        model = models.DeadLogTransaction