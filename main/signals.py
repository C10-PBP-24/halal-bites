from django.db.models.signals import post_migrate
from django.core.management import call_command
from django.apps import AppConfig

def load_fixture_data(sender, **kwargs):
    # Loading the JSON files for fixtures
    call_command('loaddata', 'foods.json')
    call_command('loaddata', 'resto.json')