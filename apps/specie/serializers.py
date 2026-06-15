from django.db import transaction
from rest_framework import serializers
from apps.specie import models
from apps.common import enums


class SpecieSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Specie
        fields = '__all__'


class SpecieGrowthStateRuleSerializer(serializers.ModelSerializer):
    warning_days = serializers.IntegerField(required=False, allow_null=True)
    danger_days = serializers.IntegerField(required=False, allow_null=True)

    class Meta:
        model = models.SpecieGrowthStateRule
        exclude = ['specie']


class SpecieBreedingRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SpecieBreedingRule
        exclude = ['specie']


class SpecieInbreedingRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SpecieInbreedingRule
        exclude = ['specie']


class SpecieFastingRuleSerializer(serializers.ModelSerializer):
    warning_days = serializers.IntegerField(required=False, allow_null=True)
    
    class Meta:
        model = models.SpecieFastingRule
        exclude = ['growth_state']


# class SpecieRuleReadSerializer(serializers.Serializer):



class SpecieRuleWriteSerializer(serializers.Serializer):
    sex = serializers.ChoiceField(enums.Sex, write_only=True)
    growth_state_rules = SpecieGrowthStateRuleSerializer(many=True, required=False)
    # fasting_rules = SpecieFastingRuleSerializer(many=True, required=False)
    breeding_rule = SpecieBreedingRuleSerializer(required=False)
    inbreeding_rule = SpecieInbreedingRuleSerializer(required=False)

    @transaction.atomic
    def update(self, instance, validated_data):
        sex = validated_data.pop('sex', None)
        growth_state_rules = validated_data.pop('growth_state_rules', [])
        breeding_rule = validated_data.pop('breeding_rule', None)
        inbreeding_rule = validated_data.pop('inbreeding_rule', None)

        instance.growth_state_rules.all().delete()
        instance.breeding_rules.all().delete()
        instance.inbreeding_rules.all().delete()

        for rule in growth_state_rules:
            warning_days = rule.pop("warning_days", None)
            danger_days = rule.pop("danger_days", None)
            note = rule.pop("note", None)

            growth_rule = models.SpecieGrowthStateRule.objects.create(specie=instance, sex=sex, **rule)
            if warning_days is not None:
                models.SpecieFastingRule.objects.create(
                    growth_state=growth_rule,
                    warning_days=warning_days,
                    danger_days=danger_days,
                    note=note,
                )

        if breeding_rule:
            models.SpecieBreedingRule.objects.create(specie=instance, sex=sex, **breeding_rule)

        if inbreeding_rule:
            models.SpecieInbreedingRule.objects.create(specie=instance, sex=sex, **inbreeding_rule)

        return instance

class GrowthStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.GrowthState
        fields = '__all__'