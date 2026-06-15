from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from framework.tests import BaseTestCase
from apps.animal import models, factories
from apps.specie.factories import SpecieFactory
from apps.breeding.factories import BreedingPairFactory, EggBatchFactory
from apps.users.factories import UserFactory
from apps.common import enums


class AnimalTestCase(BaseTestCase):
    def setUp(self):
        self.client = APIClient()
        self.client.force_authenticate(user=UserFactory())

    def test_list_animal_should_success(self):
        for i in range(3):
            factories.AnimalFactory()

        response = self.client.get(reverse('animal-list'))

        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        self.assertEqual(response.data['total'], 3)

    def test_retrieve_animal_should_success(self):
        animal = factories.AnimalFactory()
        factories.AnimalFactory()

        response = self.client.get(reverse('animal-detail', kwargs={'pk': animal.id}))

        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        self.assertEqual(response.data['id'], str(animal.id))

    def test_create_animal_should_success(self):
        specie = SpecieFactory()
        father = factories.AnimalFactory(specie=specie)
        mother = factories.AnimalFactory(specie=specie)
        breeding_pair = BreedingPairFactory(male=father, female=mother)
        egg_batch = EggBatchFactory(breeding_pair=breeding_pair)

        response = self.client.post(reverse('animal-list'), data={
            'code': 'test_code',
            'specie': specie.id,
            'sex': enums.Sex.MALE,
            'hatch_date': '2025-09-09',
            'acquisition_date': '2022-09-09',
            'origin': enums.Origin.CAPITIVE,
            'egg': egg_batch.id,
            'genetic_value_note': 'test genetic note',
            'status': enums.Status.KEEP,
            'is_assist_feed_needed': False,
            'note': 'test note',
        })

        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        created_id = response.data['id']
        animal = models.Animal.objects.get(id=created_id)
        self.assertEqual(animal.code, 'test_code')
        self.assertEqual(animal.specie, specie)
        self.assertEqual(animal.sex, 'male')
        self.assertEqual(str(animal.hatch_date), '2025-09-09')
        self.assertEqual(str(animal.acquisition_date), '2022-09-09')
        self.assertEqual(animal.genetic_value_note, 'test genetic note')
        self.assertEqual(animal.egg, egg_batch)
        self.assertEqual(animal.origin, 'captive')
        self.assertEqual(animal.status, 'keep')
        self.assertFalse(animal.is_assist_feed_needed)
        self.assertEqual(animal.note, 'test note')

    def test_update_animal_should_success(self):
        animal = factories.AnimalFactory()

        response = self.client.patch(reverse('animal-detail', kwargs={'pk': animal.id}), data={
            'code': 'test_code',
            'sex': enums.Sex.MALE,
            'genetic_value_note': 'test genetic note',
            'status': enums.Status.KEEP,
            'is_assist_feed_needed': False,
            'note': 'test note',
        })

        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        animal.refresh_from_db()
        self.assertEqual(animal.code, 'test_code')
        self.assertEqual(animal.sex, 'male')
        self.assertEqual(animal.genetic_value_note, 'test genetic note')
        self.assertEqual(animal.status, 'keep')
        self.assertFalse(animal.is_assist_feed_needed)
        self.assertEqual(animal.note, 'test note')

    def test_delete_animal_should_success(self):
        animal = factories.AnimalFactory()

        response = self.client.delete(reverse('animal-detail', kwargs={'pk': animal.id}))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT, response.data)
        self.assertFalse(models.Animal.objects.actives().filter(id=animal.id).exists())