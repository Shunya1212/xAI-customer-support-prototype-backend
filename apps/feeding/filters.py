import django_filters as filters
from django.db.models import TextChoices, Q, Case, When, IntegerField
from apps.feeding import models


class FoodFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='icontains')
    ordering = filters.OrderingFilter(
        fields=(
            ('name', 'name'),
        )
    )

    class Meta:
        model = models.Food
        fields = ['type']


class FeedingPlanFilter(filters.FilterSet):
    class Meta:
        model = models.FeedingPlan
        fields = []