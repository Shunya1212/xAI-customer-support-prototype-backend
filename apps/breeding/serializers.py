from rest_framework import serializers
from apps.breeding import models
from apps.animal.models import Animal
from apps.common import enums


class BreedingPairSerializer(serializers.ModelSerializer):
    def validate_male(self, value):
        if value.sex != enums.Sex.MALE:
            raise serializers.ValidationError({'male': 'Animal sex must be male.'})
        return value
        
    def validate_female(self, value):
        if value.sex != enums.Sex.FEMALE:
            raise serializers.ValidationError({'female': 'Animal sex must be female.'})
        return value

    class Meta:
        model = models.BreedingPair
        fields = '__all__'


class EggBatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.EggBatch
        fields = '__all__'


class EggBatchCreateNewBornSerializer(serializers.Serializer):
    pass