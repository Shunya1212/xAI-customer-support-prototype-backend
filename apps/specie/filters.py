import django_filters as filters
from apps.specie import models


class GrowthStateFilter(filters.FilterSet):
    class Meta:
        model = models.GrowthState
        fields = []


class SpecieFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='icontains')
    specific_name = filters.CharFilter(lookup_expr='icontains')
    ordering = filters.OrderingFilter(
        fields=(
            ('name', 'name'),
            ('specific_name', 'specific_name')
        )
    )

    class Meta:
        model = models.Specie
        fields = []