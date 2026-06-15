from django.db import models
from framework.models import BaseModel, BaseModelQuerySet
from apps.animal.models import Animal
from apps.common import enums


class BreedingPair(BaseModel):        
    code = models.CharField(max_length=256, unique=True)
    male = models.ForeignKey(Animal, on_delete=models.CASCADE, related_name='male_breeding_pairs')
    female = models.ForeignKey(Animal, on_delete=models.CASCADE, related_name='female_breeding_pairs')
    paring_date = models.DateField(help_text='paring date')
    status = models.CharField(choices=enums.BreedingResult.choices, default=enums.BreedingResult.IN_PROGRESS, help_text='result of breeding')
    note = models.TextField(null=True, blank=True, help_text='note')

    def __str__(self):
        return f"{self.code}"

    class Meta:
        ordering = ['-created', '-updated']
        verbose_name = 'Breeding Pair'
        verbose_name_plural = 'Breeding Pairs'


class EggBatch(BaseModel):
    code = models.CharField(max_length=256, unique=True)
    breeding_pair = models.OneToOneField(BreedingPair, on_delete=models.CASCADE, related_name='egg_batch')
    laid_date = models.DateField(help_text='egg laid date')
    laid_egg_amount = models.PositiveIntegerField(default=1, help_text='laid egg amount')
    hatched_egg_amount = models.PositiveIntegerField(null=True, blank=True, default=0, help_text='hached egg amount')
    note = models.TextField(null=True, blank=True, help_text='note')

    def __str__(self):
        return f"{self.code}"
    
    class Meta:
        ordering = ['-created', '-updated']
        verbose_name = 'Egg Batch'
        verbose_name_plural = 'Egg Batches'