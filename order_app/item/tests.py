from django.test import TestCase
from .models import Item
from django.urls import reverse


class Order_CRUD_test(TestCase):

    def setUp(self):
        self.item = Item.objects.create(name='pizza', price=800)

    def test_item_list(self):
        response = self.client.get('/items/')
        self.assertEqual(response.status_code, 200)
    
    def test_api_item_list(self):
        response = self.client.get('/api/items/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.headers['Content-Type'].startswith('application/json'))
        data = response.json()
        self.assertGreater(len(data), 0)

    def test_get_item_create(self):
        response = self.client.get(reverse('item_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'item/item_create.html')

    def test_post_item_create(self):
        item_count = Item.objects.count()
        form_data = {
            "name": "tea",
            "price": '200'
        }
        response = self.client.post(reverse('item_create'), form_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Item.objects.count(), item_count + 1)
        self.assertTrue(Item.objects.filter(name='tea').exists())
        self.assertRedirects(response, '/items/')
