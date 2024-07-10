from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Product


class UserMeEndpointTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword123')

        self.staff_user = User.objects.create_user(username='staffuser',
                                                   password='staffpassword123',
                                                   is_staff=True)

        self.user2 = User.objects.create_user(username='testuser2', password='testpassword123')

    def test_user_authentication(self):
        url = reverse('token_obtain_pair')

        response = self.client.post(url, {'username': 'testuser', 'password': 'testpassword123'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

    def test_me_endpoint(self):
        self.client.force_authenticate(self.user)
        url = reverse('user-me')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'testuser')
        self.assertEqual(response.data['email'], self.user.email)
        self.assertEqual(response.data['first_name'], self.user.first_name)
        self.assertEqual(response.data['last_name'], self.user.last_name)

    def test_profile_update(self):
        url = reverse('token_obtain_pair')

        response = self.client.post(url, {'username': 'testuser', 'password': 'testpassword123'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        token = response.data['access']

        url = reverse('user-update-me')

        email = 'test@mail.com'
        first_name = 'John'
        last_name = 'Doe'

        response = self.client.patch(url, {'email': email,
                                           'first_name': first_name,
                                           'last_name': last_name},
                                     HTTP_AUTHORIZATION=f'Bearer {token}')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        user = User.objects.get(username='testuser')
        user.refresh_from_db()

        self.assertEqual(user.email, email)
        self.assertEqual(user.first_name, first_name)
        self.assertEqual(user.last_name, last_name)

    def test_delete_own_account(self):
        url = reverse('token_obtain_pair')

        response = self.client.post(url, {'username': 'testuser', 'password': 'testpassword123'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        token = response.data['access']
        url = reverse('user-delete-user', kwargs={'pk': self.user.id})

        response = self.client.delete(url, HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_staff_delete_user_account(self):
        url = reverse('token_obtain_pair')

        response = self.client.post(url, {'username': 'staffuser', 'password': 'staffpassword123'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        token = response.data['access']
        url = reverse('user-delete-user', kwargs={'pk': self.user.id})

        response = self.client.delete(url, HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_other_user_account(self):
        self.client.force_authenticate(self.user)
        url = reverse('user-delete-user', kwargs={'pk': self.user2.id})

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class ProductViewSetTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword123')
        self.client.login(username='testuser', password='testpassword123')

        self.product1 = Product.objects.create(name='product1', price=100)
        self.product2 = Product.objects.create(name='product2', price=200)
        self.product3 = Product.objects.create(name='product3', price=300)

    def test_product_list(self):
        self.client.force_authenticate(self.user)

        url = reverse('product-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get('results')), 3)

    def test_product_filter_by_min_price(self):
        self.client.force_authenticate(self.user)

        url = reverse('product-list') + '?min_price=200'
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get('results')), 2)

    def test_product_filter_by_max_price(self):
        self.client.force_authenticate(self.user)

        url = reverse('product-list') + '?max_price=200'
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get('results')), 2)

    def test_product_filter_by_min_and_max_price(self):
        self.client.force_authenticate(self.user)

        url = reverse('product-list') + '?min_price=100&max_price=200'
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get('results')), 2)

    def test_product_filter_by_name(self):
        self.client.force_authenticate(self.user)

        url = reverse('product-list') + '?name=product1'
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get('results')), 1)
        self.assertEqual(response.data.get('results')[0]['name'], 'product1')
