from decimal import Decimal
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from framework.tests import BaseTestCase
from apps.animal import models, factories
from apps.users.factories import UserFactory


class SizeLogTransactionTestCase(BaseTestCase):
    def setUp(self):
        self.client = APIClient()
        self.client.force_authenticate(user=UserFactory())

    def test_list_size_log_should_success(self):
        for i in range(3):
            factories.SizeLogTransactionFactory()

        response = self.client.get(reverse('sizelog-list'))

        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        self.assertEqual(response.data['total'], 3)

    def test_create_size_log_should_success(self):
        animal = factories.AnimalFactory()

        response = self.client.post(reverse('sizelog-list'), data={
            'animal': animal.id,
            'weight': Decimal(2000),
            'length': Decimal(2000),
            'waist': Decimal(2000),
            'date': '2025-09-09',
            'note': 'test note',
        })

        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        created_id = response.data['id']
        size_log = models.SizeLogTransaction.objects.get(id=created_id)
        self.assertEqual(size_log.animal, animal)
        self.assertEqual(size_log.weight, Decimal(2000))
        self.assertEqual(size_log.length, Decimal(2000))
        self.assertEqual(size_log.waist, Decimal(2000))
        self.assertEqual(str(size_log.date), '2025-09-09')
        self.assertEqual(size_log.note, 'test note')