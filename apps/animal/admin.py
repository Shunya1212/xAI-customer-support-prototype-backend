from django.contrib import admin
from apps.animal import models
from framework.admin import BaseTabularInline


class SizeLogTransactionInline(BaseTabularInline):
    model = models.SizeLogTransaction
    exclude = models.SizeLogTransaction.base_attrs()


class FeedingLogTransactionInline(BaseTabularInline):
    model = models.FeedingLogTransaction
    exclude = models.FeedingLogTransaction.base_attrs()


class FeedingResultLogTransactionInline(BaseTabularInline):
    model = models.FeedingResultLogTransaction
    exclude = models.FeedingResultLogTransaction.base_attrs()


class DeadLogTransactionInline(BaseTabularInline):
    model = models.DeadLogTransaction
    exclude = models.DeadLogTransaction.base_attrs()


@admin.register(models.Animal)
class AnimalAdmin(admin.ModelAdmin):
    list_display = ['code', 'specie', 'sex', 'origin', 'status', 'is_dead', 'is_active']
    list_filter = ['specie', 'sex', 'status', 'is_active']
    search_fields = ['code']
    # autocomplete_fields = ['specie', 'egg', 'individual_feeding_plans']
    inlines = [SizeLogTransactionInline, FeedingLogTransactionInline, DeadLogTransactionInline]


# @admin.register(models.FeedingLogTransaction)
# class FeedingLogTransactionAdmin(admin.ModelAdmin):
#     list_display = ['animal', 'date', 'food', 'amount_with_unit', 'feeding_type']
#     list_filter = ['date', 'feeding_type', 'animal__specie']
#     search_fields = ['animal__code', 'note']
#     # autocomplete_fields = ['animal', 'food']
#     inlines = [FeedingResultLogTransactionInline]