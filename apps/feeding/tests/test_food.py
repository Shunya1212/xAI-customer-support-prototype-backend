from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from framework.tests import BaseTestCase
from apps.feeding import factories, models
from apps.users.factories import UserFactory
from apps.common import enums


class FoodTestCase(BaseTestCase):
    def setUp(self):
        self.client = APIClient()
        self.client.force_authenticate(user=UserFactory())

    def test_list_food_should_success(self):
        factories.FoodFactory()
        factories.FoodFactory()

        response = self.client.get(reverse('food-list'))

        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        self.assertEqual(response.data['total'], 2)

    def test_retrieve_food_should_success(self):
        food = factories.FoodFactory()
        factories.FoodFactory()

        response = self.client.get(reverse('food-detail', kwargs={'pk': food.id}))

        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        self.assertEqual(response.data['id'], str(food.id))

    def test_create_food_should_success(self):
        response = self.client.post(reverse('food-list'), data={
            'name': 'Rat',
            'type': enums.Type.LIVING_ANIMAL,
            'unit': enums.Unit.ITEM
        })

        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        created_id = response.data['id']
        food = models.Food.objects.get(id=created_id)
        self.assertEqual(food.name, 'Rat')
        self.assertEqual(food.type, enums.Type.LIVING_ANIMAL)
        self.assertEqual(food.unit, enums.Unit.ITEM)

    def test_update_food_should_success(self):
        food = factories.FoodFactory()
        response = self.client.patch(reverse('food-detail', kwargs={'pk': food.id}), data={
            'name': 'Rat',
            'type': enums.Type.LIVING_ANIMAL,
            'unit': enums.Unit.ITEM
        })

        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        food.refresh_from_db()
        self.assertEqual(food.name, 'Rat')
        self.assertEqual(food.type, enums.Type.LIVING_ANIMAL)
        self.assertEqual(food.unit, enums.Unit.ITEM)

    def test_delete_food_should_success(self):
        food = factories.FoodFactory()
        response = self.client.delete(reverse('food-detail', kwargs={'pk': food.id}))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT, response.data)
        self.assertFalse(models.Food.objects.actives().filter(id=food.id).exists())