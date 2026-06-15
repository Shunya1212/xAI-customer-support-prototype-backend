from rest_framework import viewsets
from rest_framework.decorators import action
from apps.breeding import models, serializers, filters


class BreedingPairViewSet(viewsets.ModelViewSet):
    queryset = models.BreedingPair.objects.actives().select_related('male', 'female')
    serializer_class = serializers.BreedingPairSerializer
    filterset_class = filters.BreedingPairFilter


class EggBatchViewSet(viewsets.ModelViewSet):
    queryset = models.EggBatch.objects.actives().select_related('breeding_pair')
    serializer_class = serializers.EggBatchSerializer
    filterset_class = filters.EggBatchFilter

    def get_serializer_class(self):
        if self.action == 'new_born':
            return serializers.EggBatchCreateNewBornSerializer
        return self.serializer_class

    @action(detail=True, methods=['post'], url_path='new-born')
    def new_born(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)