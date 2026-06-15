from django.contrib import admin
from apps.specie import models
from framework.admin import BaseTabularInline


class SpecieGrowthStateRuleInline(BaseTabularInline):
    model = models.SpecieGrowthStateRule
    exclude = models.SpecieGrowthStateRule.base_attrs()


class SpecieBreedingRuleInline(BaseTabularInline):
    model = models.SpecieBreedingRule
    exclude = models.SpecieBreedingRule.base_attrs()


class SpecieInbreedingRuleInline(BaseTabularInline):
    model = models.SpecieInbreedingRule
    exclude = models.SpecieInbreedingRule.base_attrs()


class SpecieFastingRuleInline(BaseTabularInline):
    model = models.SpecieFastingRule
    exclude = models.SpecieFastingRule.base_attrs()


@admin.register(models.Specie)
class SpecieAdmin(admin.ModelAdmin):
    list_display = ['name', 'specific_name', 'note', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name', 'specific_name']
    inlines = [SpecieGrowthStateRuleInline, SpecieBreedingRuleInline, SpecieInbreedingRuleInline]


@admin.register(models.GrowthState)
class GrowthStateAdmin(admin.ModelAdmin):
    list_display = ['state', 'sort_no', 'is_active']
    list_filter = ['is_active']