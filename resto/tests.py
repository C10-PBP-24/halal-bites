# resto/tests.py

from django.test import TestCase, Client
from django.urls import reverse
from authentication.models import CustomUser
from resto.models import Resto
from food.models import Food
from django.http import HttpResponse


class RestoViewsTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = CustomUser.objects.create_user(username='testuser', password='password', role='user')
        self.admin_user = CustomUser.objects.create_user(username='admin', password='admin', role='admin')
        
        # Create a client instance for testing
        self.client = Client()
        
        # Create sample data for Resto and Food models
        self.food = Food.objects.create(name='Sushi', price='20000', image='sushi.jpg', promo='10% off')
        self.resto = Resto.objects.create(nama='Sushi Place', makanan=self.food, lokasi='Bandung')

    def test_get_resto(self):
        response = self.client.get(reverse('resto:get_resto'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Sushi Place')

    def test_show_resto_user(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('resto:show_resto'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'resto/resto_user.html')
        self.assertContains(response, 'Sushi Place')

    def test_show_resto_admin(self):
        self.client.login(username='admin', password='admin')
        response = self.client.get(reverse('resto:show_resto'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'resto/resto_admin.html')
        self.assertContains(response, 'Sushi Place')

    def test_resto_detail(self):
        response = self.client.get(reverse('resto:resto_detail', args=[self.resto.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Sushi Place')

    def test_filter_resto(self):
        response = self.client.get(reverse('resto:filter_resto'), {'lokasi': 'Dago'})
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'restos': [{'pk': 1, 'nama': 'BVEGIEZ, CUPUKEIK', 'lokasi': 'Dago'}, {'pk': 4, 'nama': 'CAHAYA MAS', 'lokasi': 'Dago'}, {'pk': 10, 'nama': 'DJAKHAZ', 'lokasi': 'Dago'}, {'pk': 11, 'nama': 'HAI BILIK', 'lokasi': 'Dago'}, {'pk': 14, 'nama': 'NYAI', 'lokasi': 'Dago'}, {'pk': 20, 'nama': 'SARI TEMPE', 'lokasi': 'Dago'}, {'pk': 22, 'nama': 'APRIL', 'lokasi': 'Dago'}, {'pk': 29, 'nama': 'KOKAH', 'lokasi': 'Dago'}, {'pk': 33, 'nama': 'GARIS KUNING TEPUNG INDONESIA', 'lokasi': 'Dago'}, {'pk': 37, 'nama': 'JAVA OMBEN', 'lokasi': 'Dago'}, {'pk': 42, 'nama': 'RIESTAFOOD', 'lokasi': 'Dago'}, {'pk': 49, 'nama': 'SUMPIA IBU RUM', 'lokasi': 'Dago'}, {'pk': 61, 'nama': 'CEUYAH', 'lokasi': 'Dago'}, {'pk': 72, 'nama': 'AJ', 'lokasi': 'Dago'}, {'pk': 82, 'nama': 'PISAMALA', 'lokasi': 'Dago'}, {'pk': 85, 'nama': 'ZHAZAN', 'lokasi': 'Dago'}, {'pk': 96, 'nama': 'AYA RASA', 'lokasi': 'Dago'}, {'pk': 98, 'nama': 'NULLA LAC', 'lokasi': 'Dago'}]})

    def test_add_resto(self):
        self.client.login(username='admin', password='admin')
        response = self.client.post(reverse('resto:add_resto'), {
            'nama': 'New Resto',
            'nama_makanan': 'Pasta',
            'harga_makanan': '25000',
            'promo_makanan': '20% off',
            'image_makanan': 'pasta.jpg',
            'lokasi': 'Jakarta'
        })
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Resto.objects.filter(nama='New Resto').exists())

    def test_delete_resto(self):
        self.client.login(username='admin', password='admin')
        response = self.client.delete(reverse('resto:delete_resto', args=[self.resto.pk]))
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Resto.objects.filter(pk=self.resto.pk).exists())

    def test_show_xml(self):
        response = self.client.get(reverse('resto:show_xml'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/xml')

    def test_show_json(self):
        response = self.client.get(reverse('resto:show_json'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
