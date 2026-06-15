from rest_framework import serializers
from apps.animal import models


class AnimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Animal
        fields = '__all__'


class SizeLogTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SizeLogTransaction
        fields = '__all__'


class DeadLogTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DeadLogTransaction
        fields = '__all__'