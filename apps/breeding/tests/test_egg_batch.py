from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from framework.tests import BaseTestCase
from apps.breeding import factories, models
from apps.users.factories import UserFactory
from apps.animal.models import Animal


class BreedingTestCase(BaseTestCase):
    def setUp(self):
        self.client = APIClient()
        self.client.force_authenticate(user=UserFactory())

    def test_list_egg_batch_should_success(self):
        factories.EggBatchFactory()
        factories.EggBatchFactory()

        response = self.client.get(reverse('eggbatch-list'))

        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        self.assertEqual(response.data['total'], 2)

    def test_retrieve_egg_batch_should_success(self):
        egg = factories.EggBatchFactory()
        factories.EggBatchFactory()

        response = self.client.get(reverse('eggbatch-detail', kwargs={'pk': egg.id}))

        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        self.assertEqual(response.data['id'], str(egg.id))

    def test_create_egg_batch_should_success(self):
        pair = factories.BreedingPairFactory()
        response = self.client.post(reverse('eggbatch-list'), data={
            'code': 'test_code_001',
            'breeding_pair': pair.id,
            'laid_date': '2025-09-09',
            'laid_egg_amount': 15,
            'hatched_egg_amount': 10,
            'note': 'test note',
        })

        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        created_id = response.data['id']
        egg = models.EggBatch.objects.get(id=created_id)
        self.assertEqual(egg.code, 'test_code_001')
        self.assertEqual(egg.breeding_pair, pair)
        self.assertEqual(str(egg.laid_date), '2025-09-09')
        self.assertEqual(egg.laid_egg_amount, 15)
        self.assertEqual(egg.hatched_egg_amount, 10)
        self.assertEqual(egg.note, 'test note')

    def test_update_egg_batch_should_success(self):
        egg = factories.EggBatchFactory()
        pair = factories.BreedingPairFactory()
        response = self.client.patch(reverse('eggbatch-detail', kwargs={'pk': egg.id}), data={
            'code': 'test_code_001',
            'breeding_pair': pair.id,
            'laid_date': '2025-09-09',
            'laid_egg_amount': 15,
            'hatched_egg_amount': 10,
            'note': 'test note',
        })

        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        egg.refresh_from_db()
        self.assertEqual(egg.code, 'test_code_001')
        self.assertEqual(egg.breeding_pair, pair)
        self.assertEqual(str(egg.laid_date), '2025-09-09')
        self.assertEqual(egg.laid_egg_amount, 15)
        self.assertEqual(egg.hatched_egg_amount, 10)
        self.assertEqual(egg.note, 'test note')

    def test_delete_egg_batch_should_success(self):
        egg = factories.EggBatchFactory()
        response = self.client.delete(reverse('eggbatch-detail', kwargs={'pk': egg.id}))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT, response.data)
        self.assertFalse(models.EggBatch.objects.actives().filter(id=egg.id).exists())