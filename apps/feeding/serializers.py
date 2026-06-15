from django.db import transaction
from rest_framework import serializers
from apps.feeding import models


class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Food
        fields = '__all__'


class FeedingPlanItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FeedingPlanItem
        exclude = ['feeding_plan']


class FeedingPlanSerializer(serializers.ModelSerializer):
    items = FeedingPlanItemSerializer(many=True, required=True, allow_null=False)

    def __validate_food_item(self, items):
        food_ids = []
        for item in items:
            food = item.get('food')
            if food in food_ids:
                raise serializers.ValidationError({'items':'Same food item can not be selected.'})
            food_ids.append(food)

    def validate(self, data):
        items = data.get('items')
        self.__validate_food_item(items)
        return data

    def create(self, validated_data):
        items = validated_data.pop('items')
        plan = models.FeedingPlan.objects.create(**validated_data)
        for item in items:
            models.FeedingPlanItem.objects.create(
                feeding_plan=plan,
                **item
            )
        return plan
    
    @transaction.atomic
    def update(self, instance, validated_data):
        items = validated_data.pop('items')
        instance = super().update(instance, validated_data)
        existing_items = {item.id: item for item in instance.items.actives()}
        sent_item_ids = []
        # create or update items
        for item_data in items:
            item_id = item_data.get('id')
            if item_id and item_id in existing_items:
                item = existing_items[item_id]
                for attr, value in item_data.items():
                    setattr(item, attr, value)
                item.save()
                sent_item_ids.append(item_id)
            else:
                models.FeedingPlanItem.objects.create(feeding_plan=instance, **item_data)
        # delete items
        for item_id, item in existing_items.items():
            if item_id not in sent_item_ids:
                item.is_active = False
                item.save()
        return instance

    class Meta:
        model = models.FeedingPlan
        fields = '__all__'