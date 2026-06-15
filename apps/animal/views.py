from rest_framework import generics, viewsets
from apps.animal import models, serializers, filters


class AnimalViewSet(viewsets.ModelViewSet):
    queryset = models.Animal.objects.actives().select_related('specie')
    serializer_class = serializers.AnimalSerializer
    filterset_class = filters.AnimalFilter


class SizeLogTransactionView(generics.ListCreateAPIView):
    queryset = models.SizeLogTransaction.objects.actives().select_related('animal')
    serializer_class = serializers.SizeLogTransactionSerializer
    filterset_class = filters.SizeLogTransactionFilter


class DeadLogTransactionView(generics.ListCreateAPIView):
    queryset = models.DeadLogTransaction.objects.actives().select_related('animal')
    serializer_class = serializers.DeadLogTransactionSerializer
    filterset_class = filters.DeadLogTransactionFilter