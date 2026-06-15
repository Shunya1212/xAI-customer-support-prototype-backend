from django.shortcuts import render
from rest_framework import viewsets, views, generics, response, status
from rest_framework.decorators import action
from apps.specie import models, serializers, filters


class SpecieViewSet(viewsets.ModelViewSet):
    queryset = models.Specie.objects.actives().prefetch_related(
        'growth_state_rules', 
        'breeding_rules', 
        'inbreeding_rules',
        )
    serializer_class = serializers.SpecieSerializer
    filterset_class = filters.SpecieFilter
    
    @action(detail=True, methods=['get', 'post', 'patch'])
    def rules(self, request, pk=None):
        specie = self.get_object()
        if request.method=='GET':
            serializer = serializers.SpecieRuleReadSerializer(specie)
            return response.Response(serializer.data)

        serializer =serializers. SpecieRuleWriteSerializer(
            specie,
            data=request.data,
            partial=request.method=='PATCH'
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return response.Response(serializer.data, status=status.HTTP_201_CREATED)


class GrowthStateViewSet(viewsets.ModelViewSet):
    queryset = models.GrowthState.objects.actives()
    serializer_class = serializers.GrowthStateSerializer
    filterset_class = filters.GrowthStateFilter