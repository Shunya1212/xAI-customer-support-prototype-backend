from django.db import models
from framework.models import BaseModel, BaseModelQuerySet
from apps.common import enums


class Specie(BaseModel):
    name = models.CharField(max_length=256, help_text='name of specie')
    specific_name = models.CharField(max_length=256, null=True, blank=True, help_text='specific name of specie')
    criteria = models.CharField(choices=enums.Criteria.choices, default=enums.Criteria.WEIGHT, help_text='criteria for growth state')
    feeding_plans = models.ManyToManyField('feeding.FeedingPlan', blank=True, related_name='species')
    note = models.TextField(null=True, blank=True, help_text='note')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created', '-updated']
        verbose_name = 'Specie'
        verbose_name_plural = 'Species'


class GrowthState(BaseModel):
    state = models.CharField(max_length=256, help_text='grow state')
    sort_no = models.PositiveIntegerField(default=0, help_text='growth state order')
    note = models.TextField(null=True, blank=True, help_text='note')

    def __str__(self):
        return self.state

    class Meta:
        ordering = ['sort_no', '-created', '-updated']
        verbose_name = 'Growth State'
        verbose_name_plural = 'Growth States'


class SpecieGrowthStateRule(BaseModel):
    specie = models.ForeignKey(Specie, on_delete=models.CASCADE, related_name='growth_state_rules')
    sex = models.CharField(choices=enums.Sex.choices, null=True, blank=True, help_text='sex')
    growth_state = models.ForeignKey(GrowthState, on_delete=models.CASCADE, related_name='specie_growth_states')
    index = models.PositiveIntegerField(null=True, blank=True, default=0, help_text='index of growth state')
    min_weight = models.DecimalField(max_digits=16, decimal_places=2)
    min_age_days = models.PositiveIntegerField()
    note = models.TextField(null=True, blank=True, help_text='note')

    # min weight and min age will be calculated by last growth state
    # index calculated by min weight or age (use criteria in specie)
    # validate if min weight is not dupulicate value
    # validate if min age is not duplicate value

    def __str__(self):
        return f"{self.specie} - {self.growth_state}"
    
    class Meta:
        ordering = ['index']
        verbose_name = 'Specie Growth State Rule'
        verbose_name_plural = 'Specie Growth State Rules'


class SpecieBreedingRule(BaseModel):
    specie = models.ForeignKey(Specie, on_delete=models.CASCADE, related_name='breeding_rules')
    sex = models.CharField(choices=enums.Sex.choices, null=True, blank=True, help_text='sex')
    min_breeding_weight = models.DecimalField(null=True, max_digits=16, decimal_places=2, help_text='allow breeding weight for male')
    min_breeding_age_days = models.PositiveIntegerField(null=True, blank=True)
    rest_days = models.PositiveIntegerField(null=True, blank=True)
    note = models.TextField(null=True, blank=True, help_text='note')

    # cb_generation_threshold = 

    def __str__(self):
        return f"{self.specie} - breeding rule"

    def set_default_min_breeding_weight(self):
        # if not provided -> set growth state last object value
        pass

    class Meta:
        ordering = ['-created', '-updated']
        verbose_name = 'Specie Breeding Rule'
        verbose_name_plural = 'Specie Breeding Rules'


class SpecieInbreedingRule(BaseModel):
    specie = models.ForeignKey(Specie, on_delete=models.CASCADE, related_name='inbreeding_rules')
    sex = models.CharField(choices=enums.Sex.choices, null=True, blank=True, help_text='sex')
    max_allowed_level = models.IntegerField(
        choices=enums.InbreedingLevel.choices,
        default=enums.InbreedingLevel.COUSIN,
        help_text="Maximum allowed inbreeding level"
    )
    warning_level = models.IntegerField(
        choices=enums.InbreedingLevel.choices,
        null=True,
        blank=True,
        help_text="Warning threshold level"
    )
    note = models.TextField(null=True, blank=True, help_text='note')

    def __str__(self):
        return f"{self.specie} - inbreeding rule"
    
    def convert_F_to_level(F):
        if F >= 0.25:
            return 4
        elif F >= 0.125:
            return 3
        elif F >= 0.0625:
            return 2
        elif F > 0:
            return 1
        return 0
    
    class Meta:
        ordering = ['-created', '-updated']
        verbose_name = 'SpecieInbreedingRule'
        verbose_name_plural = 'SpecieInbreedingRules'


class SpecieFastingRule(BaseModel):
    growth_state = models.ForeignKey(SpecieGrowthStateRule, on_delete=models.CASCADE, related_name='specie_fasting_rules')
    warning_days = models.PositiveIntegerField()
    danger_days = models.PositiveIntegerField(null=True, blank=True)
    note = models.TextField(null=True, blank=True, help_text='note')

    def __str__(self):
        return f"{self.growth_state.growth_state.state} - {self.growth_state.specie} - fasting rule"
    
    class Meta:
        ordering = ['-created', '-updated']
        verbose_name = 'Specie Fasting Rule'
        verbose_name_plural = 'Specie Fasting Rules'