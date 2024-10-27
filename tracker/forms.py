from django import forms
from .models import Tracker

class AddFoodTrackingForm(forms.ModelForm):
    class Meta:
        model = Tracker
        fields = ['food', 'order_at']
        widgets = {
            'order_at': forms.DateInput(attrs={'type': 'date'}),
        }
