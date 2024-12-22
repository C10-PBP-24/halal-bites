from django import forms
from .models import Tracker
from resto.models import Resto
from food.models import Food

class AddFoodTrackingForm(forms.ModelForm):
    class Meta:
        model = Tracker
        fields = ['food', 'order_at']
        widgets = {
            'order_at': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args,**kwargs):
        user = kwargs.pop('user',None)
        super().__init__(*args, **kwargs)

        if user is not None:
            rated_food_ids = Food.objects.filter(ratings__user=user).values_list('id', flat=True)
            self.fields['restaurant'].queryset = Resto.objects.filter(makanan_id__in=rated_food_ids)
