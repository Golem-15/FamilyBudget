from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from unittest.mock import patch
from rest_framework import status
import json
import faker

from .models import Budget

fake = faker.Faker()
# client = Client()
User = get_user_model()


class AppTests(TestCase):
    def setUp(self):
        self.username_1 = fake.user_name()
        self.username_2 = fake.user_name()
        self.user_1 = User.objects.create_user(username=self.username_1, first_name=fake.first_name(), last_name=fake.last_name(), email=fake.email())
        self.user_2 = User.objects.create_user(username=self.username_2, first_name=fake.first_name(), last_name=fake.last_name(), email=fake.email())
        self.user_1.set_password('123')
        self.user_1.save()
        self.user_2.set_password('456')
        self.user_2.save()
        self.test_budget = Budget.objects.create(name='testBudget', balance=0, owner=self.user_1)


    def test_if_users_can_be_created_via_post(self):
        user_1 = User.objects.get(username=self.username_1)
        user_2 = User.objects.get(username=self.username_2)
        self.assertIsNotNone(user_1)
        self.assertIsNotNone(user_2)
        self.client.login(username=self.username_1, password='123')
        data = {
            'confirm_password': 'asd',
            'email': 'asd@asd',
            'first_name': 'asd',
            'last_name': 'asd',
            'password': 'asd',
            'username': 'ASD'
        }
        response = self.client.post(reverse('user-create'), data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_budget_creation(self):
        self.client.login(username=self.username_1, password='123')
        data = {"sharedWith":[],"incomes":[],"expenses":[],"name":"ASD"}
        response = self.client.post(reverse('budget-create'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(Budget.objects.get(name=data['name']))

    
    def test_if_not_authenticated_user_cannot_access_pages(self):
        urls = [
            '/admin/', '/home/', '/get/user_list/', '/my_account/', '/budget_app/', '/api/', '/budget_list/', '/create_budget/', '/user_list/', '/budget_details/1/', '/budget/list/', '/budget/details/1/', '/budget/create/', '/budget/update/1/', '/budget/delete/1/', '/income_and_expense_categories/', '/expense/create/', '/expense/update/1/', '/income/create/', '/income/update/1/', '/budget_income_list/1/', '/budget_expense_list/1/', '/upload_budget/'
        ]
        for url in urls:
            response = self.client.get(url)
            self.assertIn(response.status_code, [status.HTTP_302_FOUND, status.HTTP_403_FORBIDDEN, status.HTTP_404_NOT_FOUND])
        
    def test_user_cannot_see_not_shared_budget_details(self):
        self.client.login(username=self.username_2, password='456')
        response = self.client.get(reverse('budget-details', kwargs={'pk': self.test_budget.id}))
        self.assertEqual(json.loads(response.content), {})

    def test_user_can_see_own_budget_details(self):
        self.client.login(username=self.username_1, password='123')
        response = self.client.get(reverse('budget-details', kwargs={'pk': self.test_budget.id}))
        self.assertEqual(json.loads(response.content), {
            'balance': 0,
            'expenses': [],
            'id': 1,
            'incomes': [],
            'name': 'testBudget',
            'owner': self.username_1,
            'shared_with': []
            })

    def test_user_can_see_shared_budget_details(self):
        self.test_budget.shared_with.add(self.user_2)
        self.client.login(username=self.username_2, password='456')
        response = self.client.get(reverse('budget-details', kwargs={'pk': self.test_budget.id}))
        self.assertEqual(json.loads(response.content), {
            'balance': 0,
            'expenses': [],
            'id': 1,
            'incomes': [],
            'name': 'testBudget',
            'owner': self.username_1,
            'shared_with': [self.user_2.id]
            })
