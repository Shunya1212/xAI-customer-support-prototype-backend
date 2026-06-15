from django.contrib import admin
from apps.feeding import models
from framework.admin import BaseTabularInline


class FeedingPlanItemInline(BaseTabularInline):
    model = models.FeedingPlanItem
    exclude = models.FeedingPlanItem.base_attrs()


@admin.register(models.Food)
class FoodAdmin(admin.ModelAdmin):
    list_display = ['name', 'type', 'unit', 'is_active']
    list_filter = ['type', 'is_active']
    search_fields = ['name']


@admin.register(models.FeedingPlan)
class FeedingPlanAdmin(admin.ModelAdmin):
    list_display = ['name', 'frequency_days', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name']
    inlines = [FeedingPlanItemInline]