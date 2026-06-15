from rest_framework import generics, response, viewsets
from rest_framework.decorators import action
from apps.feeding import filters, models, serializers


class FoodViewSet(viewsets.ModelViewSet):
    queryset = models.Food.objects.actives()
    serializer_class = serializers.FoodSerializer
    filterset_class = filters.FoodFilter


class FeedingPlanViewSet(viewsets.ModelViewSet):
    queryset = models.FeedingPlan.objects.all().prefetch_related('items')
    serializer_class = serializers.FeedingPlanSerializer
    filterset_class = filters.FeedingPlanFilter

    @action(detail=True, methods=["POST"])
    def reactivate(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.reactivate()
        return self.retrieve(request, *args, **kwargs)