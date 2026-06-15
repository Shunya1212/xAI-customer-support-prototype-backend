from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from framework.tests import BaseTestCase
from apps.specie import models, factories
from apps.users.factories import UserFactory
from apps.common import enums


class SpecieTestCase(BaseTestCase):
    def setUp(self):
        self.client = APIClient()
        self.client.force_authenticate(user=UserFactory())

    def test_list_specie_should_success(self):
        for i in range(3):
            factories.SpecieFactory()
        
        response = self.client.get(reverse('specie-list'))

        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        self.assertEqual(response.data['total'], 3)

    def test_retrieve_specie_should_success(self):
        specie = factories.SpecieFactory()
        factories.SpecieFactory()

        response = self.client.get(reverse('specie-detail', kwargs={'pk': specie.id}))

        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        self.assertEqual(response.data['id'], str(specie.id))

    def test_create_specie_should_success(self):
        response = self.client.post(reverse('specie-list'), data={
            'name': 'ball python',
            'specific_name': 'ball python specie',
            'criteria': enums.Criteria.WEIGHT,
            'note': 'test note'
        })

        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        created_id = response.data['id']
        specie = models.Specie.objects.get(id=created_id)
        self.assertEqual(specie.name, 'ball python')
        self.assertEqual(specie.specific_name, 'ball python specie')
        self.assertEqual(specie.criteria, enums.Criteria.WEIGHT)
        self.assertEqual(specie.note, 'test note')

    def test_update_specie_should_success(self):
        specie = factories.SpecieFactory()

        response = self.client.patch(reverse('specie-detail', kwargs={'pk': specie.id}), data={
            'name': 'ball python',
            'specific_name': 'ball python specie',
            'criteria': enums.Criteria.WEIGHT,
            'note': 'test note'
        })

        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        specie.refresh_from_db()
        self.assertEqual(specie.name, 'ball python')
        self.assertEqual(specie.specific_name, 'ball python specie')
        self.assertEqual(specie.criteria, enums.Criteria.WEIGHT)
        self.assertEqual(specie.note, 'test note')
    
    def test_delete_specie_should_success(self):
        specie = factories.SpecieFactory()

        response = self.client.delete(reverse('specie-detail', kwargs={'pk': specie.id}))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT, response.data)
        self.assertFalse(models.Specie.objects.actives().filter(id=specie.id).exists())