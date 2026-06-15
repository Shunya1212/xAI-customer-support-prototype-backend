from decimal import Decimal
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from framework.tests import BaseTestCase
from apps.specie import models, factories
from apps.users.factories import UserFactory
from apps.common import enums


class SpecieRulesTestCase(BaseTestCase):
    def setUp(self):
        self.client = APIClient()
        self.client.force_authenticate(user=UserFactory())

    # def test_retrieve_specie_rules_should_success(self):
    #     specie = factories.SpecieFactory()
    #     factories.SpecieFactory()

    #     response = self.client.get(reverse('specie-detail', kwargs={'pk': specie.id}))

    #     self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
    #     self.assertEqual(response.data['id'], str(specie.id))

    def test_create_specie_rules_should_success(self):
        specie = factories.SpecieFactory()
        baby = factories.GrowthStateFactory(state='baby')
        adult = factories.GrowthStateFactory(state='adult')
        response = self.client.post(reverse('specie-rules', kwargs={'pk': specie.id}), data={
            "sex": enums.Sex.MALE,
            "growth_state_rules": [
                {
                "growth_state": baby.id,
                "index": 1,
                "min_weight": Decimal(100),
                "min_age_days": 30,
                "warning_days": 7,
                "danger_days": 14
                },
                {
                "growth_state": adult.id,
                "index": 2,
                "min_weight": Decimal(4000),
                "min_age_days": 300,
                "warning_days": 15,
                "danger_days": 30
                },
            ],
            "breeding_rule": {
                "min_breeding_weight": Decimal(500),
                "min_breeding_age_days": 365,
                "rest_days": 150
            },
            "inbreeding_rule": {
                "max_allowed_level": enums.InbreedingLevel.COUSIN,
                "warning_level": enums.InbreedingLevel.CLOSE,
            },
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        growth_rules = models.SpecieGrowthStateRule.objects.actives()
        fasting_rules = models.SpecieFastingRule.objects.actives()
        breeding_rule = models.SpecieBreedingRule.objects.actives().first()
        inbreeding_rule = models.SpecieInbreedingRule.objects.actives().first()
        # check growth rules
        self.assertEqual(growth_rules[0].specie, specie)
        self.assertEqual(growth_rules[0].sex, enums.Sex.MALE)
        self.assertEqual(growth_rules[0].growth_state, baby)
        self.assertEqual(growth_rules[0].index, 1)
        self.assertEqual(growth_rules[0].min_weight, Decimal(100))
        self.assertEqual(growth_rules[0].min_age_days, 30)
        self.assertEqual(growth_rules[1].specie, specie)
        self.assertEqual(growth_rules[1].sex, enums.Sex.MALE)
        self.assertEqual(growth_rules[1].growth_state, adult)
        self.assertEqual(growth_rules[1].index, 2)
        self.assertEqual(growth_rules[1].min_weight, Decimal(4000))
        self.assertEqual(growth_rules[1].min_age_days, 300)

        # check fasting rules
        self.assertEqual(fasting_rules[0].growth_state, growth_rules[1])
        self.assertEqual(fasting_rules[0].warning_days, 15)
        self.assertEqual(fasting_rules[0].danger_days, 30)
        self.assertEqual(fasting_rules[1].growth_state, growth_rules[0])
        self.assertEqual(fasting_rules[1].warning_days, 7)
        self.assertEqual(fasting_rules[1].danger_days, 14)

        # check breeding rule
        self.assertEqual(breeding_rule.specie, specie) 
        self.assertEqual(breeding_rule.sex, enums.Sex.MALE) 
        self.assertEqual(breeding_rule.min_breeding_weight, Decimal(500)) 
        self.assertEqual(breeding_rule.min_breeding_age_days, 365) 
        self.assertEqual(breeding_rule.rest_days, 150)

        # check inbreeding rule
        self.assertEqual(inbreeding_rule.specie, specie)
        self.assertEqual(inbreeding_rule.sex, enums.Sex.MALE)
        self.assertEqual(inbreeding_rule.max_allowed_level, enums.InbreedingLevel.COUSIN)
        self.assertEqual(inbreeding_rule.warning_level, enums.InbreedingLevel.CLOSE)

    # def test_update_specie_rules_should_success(self):
    #     specie = factories.SpecieFactory()

    #     response = self.client.patch(reverse('specie-detail', kwargs={'pk': specie.id}), data={
    #         'name': 'ball python',
    #         'specific_name': 'ball python specie',
    #         'criteria': models.Specie.Criteria.WEIGHT,
    #         'note': 'test note'
    #     })

    #     self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
    #     specie.refresh_from_db()
    #     self.assertEqual(specie.name, 'ball python')
    #     self.assertEqual(specie.specific_name, 'ball python specie')
    #     self.assertEqual(specie.criteria, models.Specie.Criteria.WEIGHT)
    #     self.assertEqual(specie.note, 'test note')