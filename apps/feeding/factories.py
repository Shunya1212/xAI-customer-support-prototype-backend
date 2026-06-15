import factory
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyChoice
from apps.feeding import models


class FoodFactory(DjangoModelFactory):
    name = factory.Faker('word')
    type = FuzzyChoice(models.Food.Type.choices)
    unit = FuzzyChoice(models.Food.Unit.choices)

    class Meta:
        model = models.Food


class FeedingPlanFactory(DjangoModelFactory):
    name = factory.Faker('word')

    class Meta:
        model = models.FeedingPlan


class FeedingPlanItemFactory(DjangoModelFactory):
    food = factory.SubFactory(FoodFactory)
    feeding_plan = factory.SubFactory(FeedingPlanFactory)
    amount = factory.Faker('pyint', min_value=1, max_value=20)

    class Meta:
        model = models.FeedingPlanItem