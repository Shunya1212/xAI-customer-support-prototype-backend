from django.db import models
from framework.models import BaseModel, BaseModelQuerySet
from apps.specie.models import Specie
from apps.animal.models import Animal
from apps.common import enums


class Food(BaseModel):
    name = models.CharField(max_length=256, help_text='food')
    type = models.CharField(choices=enums.Type.choices, default=enums.Type.OTHER, help_text='food type')
    unit = models.CharField(choices=enums.Unit.choices, default=enums.Unit.ITEM, help_text='food amount unit')

    def __str__(self):
        return f"{self.name}"
    
    class Meta:
        ordering = ['-created', '-updated']
        verbose_name = 'Food'
        verbose_name_plural = 'Foods'
    

class FeedingPlan(BaseModel):
    name = models.CharField(max_length=256, help_text='name of feeding plan')
    frequency_days = models.PositiveIntegerField(null=True, blank=True)
    note = models.TextField(null=True, blank=True, help_text='note')

    def __str__(self):
        return f"{self.name}"

    def reactivate(self):
        self.is_active = True
        self.save()
    
    class Meta:
        ordering = ['-created', '-updated']
        verbose_name = 'Feeding Plan'
        verbose_name_plural = 'Feeding Plans'


class FeedingPlanItem(BaseModel):
    food = models.ForeignKey(Food, on_delete=models.CASCADE, related_name='feeding_plan_items')
    feeding_plan = models.ForeignKey(FeedingPlan, on_delete=models.CASCADE, related_name='items')
    amount = models.PositiveIntegerField(default=1, help_text='item amount')

    def __str__(self):
        return f"{self.feeding_plan} - {self.food}"
    
    @property
    def amount_with_unit(self):
        return f"{self.amount} {self.food.unit}"
    
    class Meta:
        ordering = ['-created', '-updated']
        verbose_name = 'Feeding Plan Item'
        verbose_name_plural = 'Feeding Plan Items'