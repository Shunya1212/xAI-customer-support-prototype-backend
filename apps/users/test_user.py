from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from apps.users.factories import GroupFactory, UserFactory
from framework.tests import BaseTestCase
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model


User = get_user_model()


class UserTestCase(BaseTestCase):
    def setUp(self):
        self.client = APIClient()
        self.groups = [
            GroupFactory(name='group1'),
            GroupFactory(name='group2'),
            GroupFactory(name='group3')
        ]
        self.users = [
            UserFactory(
                first_name='Johnie',
                last_name='Doe',
                username='j0hn',
                groups=[self.groups[0], self.groups[1]],
                email='john.doe@example.com'
            ),
            UserFactory(first_name="Dosh", last_name="Joe", groups=[self.groups[0]]),
            UserFactory(first_name="Zhong", last_name="Xina", groups=[self.groups[0]]),
        ]
        self.client.force_authenticate(user=self.users[0])

    def test_create_user_should_success(self):
        group1 = Group.objects.create(name="qc")
        group2 = Group.objects.create(name="wt")

        response = self.client.post(reverse('user-list'), data={
            "username": "test_user",
            "first_name": "test_first",
            "last_name": "test_last",
            "password": "password123",
            "groups": [group1.name, group2.name]
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = User.objects.get(username="test_user")
        self.assertEqual(user.full_name, "test_first test_last")
        self.assertEqual(list(user.groups.all()), [group1, group2])

    def test_change_password_should_success(self):
        response = self.client.post(reverse('change-password'), data={
            "old_password": "password",
            "new_password": "new_password123"
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.users[0].refresh_from_db()
        self.assertTrue(self.users[0].check_password("new_password123"))