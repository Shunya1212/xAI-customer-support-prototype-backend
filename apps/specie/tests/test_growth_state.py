from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from framework.tests import BaseTestCase
from apps.specie import models, factories
from apps.users.factories import UserFactory


class GrowthStateTestCase(BaseTestCase):
    def setUp(self):
        self.client = APIClient()
        self.client.force_authenticate(user=UserFactory())

    def test_list_growth_state_should_success(self):
        factories.GrowthStateFactory(sort_no=2)
        factories.GrowthStateFactory(sort_no=1)
        factories.GrowthStateFactory(sort_no=3)

        response = self.client.get(reverse('growthstate-list'))

        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        self.assertEqual(response.data['total'], 3)
        self.assertEqual(response.data['results'][0]['sort_no'], 1)
        self.assertEqual(response.data['results'][1]['sort_no'], 2)
        self.assertEqual(response.data['results'][2]['sort_no'], 3)

    def test_retrieve_growth_state_should_success(self):
        growth_state = factories.GrowthStateFactory()
        factories.GrowthStateFactory()

        response = self.client.get(reverse('growthstate-detail', kwargs={'pk': growth_state.id}))

        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        self.assertEqual(response.data['id'], str(growth_state.id))
        self.assertEqual(response.data['state'], growth_state.state)
        self.assertEqual(response.data['sort_no'], growth_state.sort_no)
    
    def test_create_growth_state_should_success(self):
        response = self.client.post(reverse('growthstate-list'), data={
            'state': 'baby',
            'sort_no': 1,
            'note': 'test note'
        })

        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        created_id = response.data['id']
        growth_state = models.GrowthState.objects.get(id=created_id)
        self.assertEqual(growth_state.state, 'baby')
        self.assertEqual(growth_state.sort_no, 1)
        self.assertEqual(growth_state.note, 'test note')

    def test_update_growth_state_should_success(self):
        growth_state = factories.GrowthStateFactory()

        response = self.client.patch(reverse('growthstate-detail', kwargs={'pk': growth_state.id}), data={
            'state': 'baby',
            'sort_no': 1,
            'note': 'test note'
        })

        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        growth_state.refresh_from_db()
        self.assertEqual(growth_state.state, 'baby')
        self.assertEqual(growth_state.sort_no, 1)
        self.assertEqual(growth_state.note, 'test note')
    
    def test_delete_growth_state_should_success(self):
        growth_state = factories.GrowthStateFactory()

        response = self.client.delete(reverse('growthstate-detail', kwargs={'pk': growth_state.id}))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT, response.data)
        self.assertFalse(models.GrowthState.objects.actives().filter(id=growth_state.id).exists())