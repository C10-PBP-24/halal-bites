from django.test import TestCase, Client, SimpleTestCase
from django.urls import reverse, resolve
from django.contrib.auth import get_user_model, models as auth_models
from django.apps import apps
from food.models import Food
from rating.models import Rating
from rating.forms import RatingForm
from rating.views import create_rating, rated_foods
from rating.apps import RatingConfig
import uuid
import django
from django.db import connection
from django.db.migrations.executor import MigrationExecutor
from django.db.utils import OperationalError


class RatingModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpass'
        )
        self.food = Food.objects.create(
            name='Test Food',
            description='Test Description'
        )
        self.rating = Rating.objects.create(
            food=self.food,
            user=self.user,
            rating=4,
            description='Test Description'
        )

    def test_rating_creation(self):
        self.assertEqual(self.rating.food, self.food)
        self.assertEqual(self.rating.user, self.user)
        self.assertEqual(self.rating.rating, 4)
        self.assertEqual(self.rating.description, 'Test Description')
        self.assertIsInstance(self.rating.id, uuid.UUID)

    def test_rating_str(self):
        self.assertEqual(str(self.rating), f"{self.food.name} - {self.rating.rating} by {self.user.username}")

    def test_rating_min_value(self):
        self.rating.rating = 1
        self.rating.save()
        self.assertEqual(self.rating.rating, 1)

    def test_rating_max_value(self):
        self.rating.rating = 5
        self.rating.save()
        self.assertEqual(self.rating.rating, 5)

    def test_rating_below_min_value(self):
        with self.assertRaises(Exception):
            self.rating.rating = 0
            self.rating.save()

    def test_rating_above_max_value(self):
        with self.assertRaises(Exception):
            self.rating.rating = 6
            self.rating.save()

    def test_rating_related_name(self):
        self.assertEqual(self.user.ratings.first(), self.rating)
        self.assertEqual(self.food.ratings.first(), self.rating)

class RatingFormTest(TestCase):
    def test_rating_form_valid_data(self):
        form = RatingForm(data={
            'rating': '5',
            'description': 'Excellent!'
        })

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['rating'], '5')
        self.assertEqual(form.cleaned_data['description'], 'Excellent!')

    def test_rating_form_invalid_data(self):
        form = RatingForm(data={
            'rating': '6',  # Invalid rating, should be between 1 and 5
            'description': 'Invalid rating'
        })

        self.assertFalse(form.is_valid())
        self.assertIn('rating', form.errors)

    def test_rating_form_empty_data(self):
        form = RatingForm(data={})

        self.assertFalse(form.is_valid())
        self.assertIn('rating', form.errors)
        self.assertIn('description', form.errors)

    def test_rating_form_missing_description(self):
        form = RatingForm(data={
            'rating': '5',
            'description': ''
        })

        self.assertFalse(form.is_valid())
        self.assertIn('description', form.errors)

class RatingViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = auth_models.User.objects.create_user(username='testuser', password='12345')
        self.food = Food.objects.create(name='Test Food', description='Test Description')
        self.create_rating_url = reverse('rating:create_rating', args=[self.food.id])
        self.rated_foods_url = reverse('rating:rated_foods')

    def test_create_rating_view_get(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(self.create_rating_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'rating_form.html')

    def test_create_rating_view_post_valid(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(self.create_rating_url, {
            'rating': 5,
            'description': 'Great food!'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.rated_foods_url)
        self.assertTrue(Rating.objects.filter(food=self.food, user=self.user).exists())

    def test_create_rating_view_post_invalid(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(self.create_rating_url, {
            'rating': '',
            'description': ''
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'rating_form.html')
        self.assertFalse(Rating.objects.filter(food=self.food, user=self.user).exists())

    def test_create_rating_view_unauthenticated(self):
        response = self.client.get(self.create_rating_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'/accounts/login/?next={self.create_rating_url}')

    def test_rated_foods_view(self):
        Rating.objects.create(food=self.food, user=self.user, rating=5, description='Great food!')
        response = self.client.get(self.rated_foods_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'rated_foods.html')
        self.assertContains(response, self.food.name)

    def test_rated_foods_view_empty(self):
        response = self.client.get(self.rated_foods_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'rated_foods.html')
        self.assertContains(response, 'No rated foods available.')

    def test_create_rating_view_invalid_food(self):
        self.client.login(username='testuser', password='12345')
        invalid_food_url = reverse('rating:create_rating', args=[999])
        response = self.client.get(invalid_food_url)
        self.assertEqual(response.status_code, 404)

class TestUrls(SimpleTestCase):
    def test_create_rating_url_is_resolved(self):
        url = reverse('rating:create_rating', args=[1])
        self.assertEquals(resolve(url).func, create_rating)

    def test_rated_foods_url_is_resolved(self):
        url = reverse('rating:rated_foods')
        self.assertEquals(resolve(url).func, rated_foods)

class RatingConfigTest(TestCase):
    def test_apps(self):
        self.assertEqual(RatingConfig.name, 'rating')
        self.assertEqual(apps.get_app_config('rating').name, 'rating')

class TestMigration0003(TestCase):
    migrate_from = ('rating', '0002_alter_rating_rating')
    migrate_to = ('rating', '0003_remove_rating_user')

    def setUp(self):
        super().setUp()
        self.apply_migration(self.migrate_from)

    def apply_migration(self, target):
        executor = MigrationExecutor(connection)
        executor.migrate([target])

    def test_field_removed(self):
        self.apply_migration(self.migrate_to)
        with connection.cursor() as cursor:
            try:
                cursor.execute("SELECT user FROM rating_rating")
            except OperationalError as e:
                self.assertIn('no such column: user', str(e))

class MigrationTestCase(TestCase):
    def test_migration_0005_alter_rating_user(self):
        applied_migrations = connection.migration_recorder.applied_migrations()
        self.assertIn(('rating', '0005_alter_rating_user'), applied_migrations)

        User = get_user_model()
        Rating = self.get_model('rating', 'Rating')
        user_field = Rating._meta.get_field('user')

        self.assertTrue(user_field.default)
        self.assertEqual(user_field.default(), uuid.uuid4())
        self.assertEqual(user_field.on_delete, django.db.models.deletion.CASCADE)
        self.assertEqual(user_field.related_name, 'ratings')
        self.assertEqual(user_field.remote_field.model, User)

    def get_model(self, app_label, model_name):
        try:
            with connection.schema_editor() as schema_editor:
                return schema_editor.connection.introspection.get_table_description(
                    schema_editor.connection.cursor(), model_name
                )
        except OperationalError:
            self.fail(f"Model {model_name} does not exist in app {app_label}")
