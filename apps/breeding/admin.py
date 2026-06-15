from django.contrib import admin
from apps.breeding import models


@admin.register(models.BreedingPair)
class BreedingPairAdmin(admin.ModelAdmin):
    list_display = ['code', 'male', 'female', 'paring_date', 'status', 'is_active']
    list_filter = ['status', 'is_active']
    search_fields = ['code', 'male', 'female']


@admin.register(models.EggBatch)
class EggBatchAdmin(admin.ModelAdmin):
    list_display = ['code', 'breeding_pair', 'laid_date', 'laid_egg_amount', 'hatched_egg_amount', 'is_active']
    list_filter = ['breeding_pair', 'is_active']
    search_fields = ['code']