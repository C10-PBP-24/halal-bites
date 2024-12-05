from django.forms import ModelForm
from food.models import Food
from django.utils.html import strip_tags

class FoodEntryForm(ModelForm):
    class Meta:
        model = Food
        fields = ["name", "price", "image", "price"]