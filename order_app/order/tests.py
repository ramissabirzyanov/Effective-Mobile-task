from django.test import TestCase
from .models import Order, OrderItem
from order_app.item.models import Item
from django.urls import reverse


class Order_CRUD_test(TestCase):

    def setUp(self):
        self.item1 = Item.objects.create(name='pizza', price=800)
        self.item2 = Item.objects.create(name='cola', price=200)
        self.order = Order.objects.create(
            table_number=5,
            status ='waiting')
        OrderItem.objects.create(order=self.order, item=self.item1, quantity=2)
        OrderItem.objects.create(order=self.order, item=self.item2, quantity=3)
        self.order.calculate_total_price()

    def test_order_list(self):
        response = self.client.get('/orders/')
        self.assertEqual(response.status_code, 200)
    
    def test_api_order_list(self):
        response = self.client.get('/api/orders/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.headers['Content-Type'].startswith('application/json'))
        data = response.json()
        self.assertGreater(len(data), 0)

    def test_get_order_create(self):
        response = self.client.get(reverse('order_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'order/order_create.html')

    def test_post_order_create(self):
        task_count = Order.objects.count()
        form_data = {
            'table_number': '8',
            'status': 'waiting',
            f'item_{self.item2.id}': '1',
        }
        response = self.client.post(reverse('order_create'), form_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Order.objects.count(), task_count + 1)
        self.assertTrue(Order.objects.filter(table_number=8).exists())
        self.assertRedirects(response, '/orders/')
        order = Order.objects.get(table_number=8)
        order_detail = self.client.get(reverse('order_detail', args=[order.id]))
        self.assertEqual(order_detail.status_code, 200)

    def test_get_order_update(self):
        response = self.client.get(reverse('order_update', args=[self.order.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'order/order_update.html')

    def test_post_order_update(self):
        new_form_data = {
            'table_number': '5',
            'status': 'paid',
            f'item_{self.item1.id}': '1',
        }
        response = self.client.post(
            reverse('order_update', args=[self.order.id]), new_form_data)
        self.order.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.order.status, 'paid')
        self.assertRedirects(response, f'/orders/{self.order.id}/')

    def test_get_order_delete(self):
        response = self.client.get(reverse('order_delete', args=[self.order.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'order/order_delete.html')

    def test_post_order_delete(self):
        response = self.client.delete(
            reverse('order_delete', args=[self.order.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/orders/')
        self.assertEqual(Order.objects.count(), 0)
