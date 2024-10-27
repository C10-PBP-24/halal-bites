from django.test import TestCase

from django.test import TestCase
from django import forms
from .forms import CustomUserCreationForm, CustomAuthenticationForm
# from .models import CustomUser

class CustomUserCreationFormTest(TestCase):
    def test_form_fields(self):
        form = CustomUserCreationForm()
        self.assertIn('username', form.fields)
        self.assertIn('password1', form.fields)
        self.assertIn('password2', form.fields)
        self.assertIn('role', form.fields)

    def test_form_widgets(self):
        form = CustomUserCreationForm()
        self.assertIsInstance(form.fields['username'].widget, forms.TextInput)
        self.assertIsInstance(form.fields['password1'].widget, forms.PasswordInput)
        self.assertIsInstance(form.fields['password2'].widget, forms.PasswordInput)
        self.assertIsInstance(form.fields['role'].widget, forms.Select)

    def test_form_error_messages(self):
        form = CustomUserCreationForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['username'], ['Username is required.'])
        self.assertEqual(form.errors['password1'], ['Password is required.'])
        self.assertEqual(form.errors['password2'], ['Password confirmation is required.'])

class CustomAuthenticationFormTest(TestCase):
    def test_form_fields(self):
        form = CustomAuthenticationForm()
        self.assertIn('username', form.fields)
        self.assertIn('password', form.fields)

    def test_form_widgets(self):
        form = CustomAuthenticationForm()
        self.assertIsInstance(form.fields['username'].widget, forms.TextInput)
        self.assertIsInstance(form.fields['password'].widget, forms.PasswordInput)

from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import UserProfile

class CustomUserModelTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpass123',
            role='user'
        )

    def test_custom_user_creation(self):
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.role, 'user')
        self.assertTrue(self.user.check_password('testpass123'))
        self.assertIsNotNone(self.user.id)

    def test_custom_user_str(self):
        self.assertEqual(str(self.user), 'testuser')

class UserProfileModelTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpass123',
            role='user'
        )
        self.user_profile = UserProfile.objects.create(user=self.user)

    def test_user_profile_creation(self):
        self.assertEqual(self.user_profile.user.username, 'testuser')
        self.assertIsNotNone(self.user_profile.id)

    def test_user_profile_str(self):
        self.assertEqual(str(self.user_profile), 'testuser')

from django.test import SimpleTestCase
from django.urls import reverse, resolve
from .views import register, user_login, logout_view

class TestUrls(SimpleTestCase):

    def test_register_url_is_resolved(self):
        url = reverse('register')
        self.assertEqual(resolve(url).func, register)

    def test_login_url_is_resolved(self):
        url = reverse('login')
        self.assertEqual(resolve(url).func, user_login)

    def test_logout_url_is_resolved(self):
        url = reverse('logout')
        self.assertEqual(resolve(url).func, logout_view)

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from authentication.models import UserProfile
from authentication.forms import CustomUserCreationForm, CustomAuthenticationForm

class AuthenticationViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')
        self.home_url = reverse('home')
        self.user_data = {
            'username': 'testuser',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        }
        self.user = User.objects.create_user(username='testuser', password='testpassword123')

    def test_register_view_get(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')
        self.assertIsInstance(response.context['form'], CustomUserCreationForm)

    def test_register_view_post(self):
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.login_url)
        self.assertTrue(User.objects.filter(username='testuser').exists())
        self.assertTrue(UserProfile.objects.filter(user__username='testuser').exists())

    def test_login_view_get(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')
        self.assertIsInstance(response.context['form'], CustomAuthenticationForm)

    def test_login_view_post(self):
        response = self.client.post(self.login_url, {'username': 'testuser', 'password': 'testpassword123'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.home_url)

    def test_logout_view(self):
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.get(self.logout_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.home_url)

from django.test import TestCase
from django.contrib.auth import get_user_model
from authentication.models import UserProfile

class CustomUserModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='password123',
            email='testuser@example.com',
            first_name='Test',
            last_name='User',
            role='user',
            city='Test City'
        )

    def test_user_creation(self):
        self.assertEqual(self.user.username, 'testuser')
        self.assertTrue(self.user.check_password('password123'))
        self.assertEqual(self.user.email, 'testuser@example.com')
        self.assertEqual(self.user.first_name, 'Test')
        self.assertEqual(self.user.last_name, 'User')
        self.assertEqual(self.user.role, 'user')
        self.assertEqual(self.user.city, 'Test City')

    def test_user_str(self):
        self.assertEqual(str(self.user), 'testuser')

class UserProfileModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='password123',
            email='testuser@example.com'
        )
        self.user_profile = UserProfile.objects.create(
            user=self.user,
            full_name='Test User'
        )

    def test_user_profile_creation(self):
        self.assertEqual(self.user_profile.user.username, 'testuser')
        self.assertEqual(self.user_profile.full_name, 'Test User')

    def test_user_profile_str(self):
        self.assertEqual(str(self.user_profile), 'Test User')

from django.test import TestCase
from django.db import connection
from django.db.utils import OperationalError

import uuid

class MigrationTestCase(TestCase):
    def test_migration_0002(self):
        # Check if the migration has been applied
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1 FROM authentication_userprofile LIMIT 1;")
        except OperationalError:
            self.fail("Migration 0002_userprofile_rated_foods_userprofile_tracked_foods_and_more has not been applied.")

        # Check if the 'rated_foods' field exists in the 'userprofile' table
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT rated_foods FROM authentication_userprofile LIMIT 1;")
        except OperationalError:
            self.fail("Field 'rated_foods' does not exist in 'userprofile' table.")

        # Check if the 'tracked_foods' field exists in the 'userprofile' table
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT tracked_foods FROM authentication_userprofile LIMIT 1;")
        except OperationalError:
            self.fail("Field 'tracked_foods' does not exist in 'userprofile' table.")

        # Check if the 'id' field in 'customuser' table is a UUID
        with connection.cursor() as cursor:
            cursor.execute("SELECT id FROM authentication_customuser LIMIT 1;")
            row = cursor.fetchone()
            self.assertIsInstance(row[0], uuid.UUID, "Field 'id' in 'customuser' table is not a UUID.")

        # Check if the 'id' field in 'userprofile' table is a UUID
        with connection.cursor() as cursor:
            cursor.execute("SELECT id FROM authentication_userprofile LIMIT 1;")
            row = cursor.fetchone()
            self.assertIsInstance(row[0], uuid.UUID, "Field 'id' in 'userprofile' table is not a UUID.")

from django.test import TestCase
from django.db import connection
from django.db.utils import OperationalError

class MigrationTestCase(TestCase):
    def test_remove_city_field(self):
        with connection.cursor() as cursor:
            try:
                cursor.execute("SELECT city FROM authentication_customuser")
                self.fail("Field 'city' should not exist in 'authentication_customuser' table.")
            except OperationalError:
                pass  # Expected behavior, field should not exist

from django.test import TestCase
from django.db import connection
from django.db.utils import OperationalError

class MigrationTestCase(TestCase):
    def test_migration_0004(self):
        # Check if the migration has been applied
        applied_migrations = connection.migration_recorder.applied_migrations()
        self.assertIn(('authentication', '0004_rename_full_name_userprofile_username'), applied_migrations)

        # Check if the field has been renamed
        with connection.cursor() as cursor:
            try:
                cursor.execute("SELECT username FROM authentication_userprofile")
            except OperationalError:
                self.fail("The field 'username' does not exist in 'authentication_userprofile' table.")

from django.test import TestCase
from django.db import connection
from django.db.utils import OperationalError

class MigrationTestCase(TestCase):
    def test_remove_username_field(self):
        with connection.cursor() as cursor:
            try:
                cursor.execute("SELECT username FROM authentication_userprofile")
                self.fail("The 'username' field should have been removed.")
            except OperationalError:
                pass  # Expected outcome, the field should not exist