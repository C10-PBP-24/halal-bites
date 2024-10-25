from django import forms
from .models import Rating

class RatingForm(forms.ModelForm):
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]

    rating = forms.ChoiceField(choices=RATING_CHOICES)

    class Meta:
        model = Rating
        fields = ['rating', 'description']