from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from framework.tests import BaseTestCase
from apps.animal import models, factories
from apps.users.factories import UserFactory
from apps.common import enums


class DeadLogTransactionTestCase(BaseTestCase):
    def setUp(self):
        self.client = APIClient()
        self.client.force_authenticate(user=UserFactory())

    def test_list_dead_log_should_success(self):
        for i in range(3):
            factories.DeadLogTransactionFactory()

        response = self.client.get(reverse('deadlog-list'))

        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        self.assertEqual(response.data['total'], 3)

    def test_create_dead_log_should_success(self):
        animal = factories.AnimalFactory()

        response = self.client.post(reverse('deadlog-list'), data={
            'animal': animal.id,
            'date': '2025-09-09',
            'cause': enums.Cause.OLD_AGE,
            'note': 'test note',
        })

        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        created_id = response.data['id']
        log = models.DeadLogTransaction.objects.get(id=created_id)
        self.assertEqual(log.animal, animal)
        self.assertEqual(str(log.date), '2025-09-09')
        self.assertEqual(log.cause, enums.Cause.OLD_AGE)
        self.assertEqual(log.note, 'test note')