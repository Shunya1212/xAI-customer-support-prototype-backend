from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from framework.tests import BaseTestCase
from apps.feeding import factories, models
from apps.users.factories import UserFactory


class FeedingPlanTestCase(BaseTestCase):
    def setUp(self):
        self.client = APIClient()
        self.client.force_authenticate(user=UserFactory())

    def test_list_feeding_plan_should_success(self):
        for i in range(3):
            factories.FeedingPlanFactory()

        response = self.client.get(reverse('feedingplan-list'))

        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        self.assertEqual(response.data['total'], 3)

    def test_retrieve_feeding_plan_should_success(self):
        plan = factories.FeedingPlanFactory()
        factories.FeedingPlanFactory()

        response = self.client.get(reverse('feedingplan-detail', kwargs={'pk': plan.id}))

        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        self.assertEqual(response.data['id'], str(plan.id))

    def test_create_feeding_plan_should_success(self):
        food_1 = factories.FoodFactory()
        food_2 = factories.FoodFactory()
        response = self.client.post(reverse('feedingplan-list'), data={
            'name': 'plan_A',
            'frequency_days': 5,
            'note': 'test note',
            'items': [
                {'food': food_1.id, 'amount': 5},
                {'food': food_2.id, 'amount': 10},
            ]
        },format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        created_id = response.data['id']
        plan = models.FeedingPlan.objects.get(id=created_id)
        items = plan.items.actives()
        self.assertEqual(plan.name, 'plan_A')
        self.assertEqual(plan.frequency_days, 5)
        self.assertEqual(plan.note, 'test note')
        self.assertEqual(items.count(), 2)
        self.assertEqual(items[0].food, food_2)
        self.assertEqual(items[0].amount, 10)
        self.assertEqual(items[1].food, food_1)
        self.assertEqual(items[1].amount, 5)

    def test_update_feeding_plan_should_success(self):
        plan = factories.FeedingPlanFactory()
        food_1 = factories.FoodFactory()
        food_2 = factories.FoodFactory()
        food_3 = factories.FoodFactory()
        factories.FeedingPlanItemFactory(feeding_plan=plan, food=food_1)
        factories.FeedingPlanItemFactory(feeding_plan=plan, food=food_2)
        response = self.client.patch(reverse('feedingplan-detail', kwargs={'pk': plan.id}), data={
            'name': 'plan_A',
            'frequency_days': 5,
            'note': 'test note',
            'items': [
                {'food': food_1.id, 'amount': 5},
                {'food': food_3.id, 'amount': 15},
            ]
        },format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        plan.refresh_from_db()
        items = plan.items.actives()
        self.assertEqual(plan.name, 'plan_A')
        self.assertEqual(plan.frequency_days, 5)
        self.assertEqual(plan.note, 'test note')
        self.assertEqual(items.count(), 2)
        self.assertEqual(items[0].food, food_3)
        self.assertEqual(items[0].amount, 15)
        self.assertEqual(items[1].food, food_1)
        self.assertEqual(items[1].amount, 5)

    def test_delete_feeding_plan_should_success(self):
        plan = factories.FeedingPlanFactory()
        response = self.client.delete(reverse('feedingplan-detail', kwargs={'pk': plan.id}))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT, response.data)
        self.assertFalse(models.FeedingPlan.objects.actives().filter(id=plan.id).exists())

    def test_reactivate_feeding_plan_should_success(self):
        plan = factories.FeedingPlanFactory(is_active=False)
        self.assertFalse(plan.is_active)
        response = self.client.post(reverse('feedingplan-reactivate', kwargs={'pk': plan.id}))
        plan.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        self.assertTrue(plan.is_active)