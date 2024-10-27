from django.forms import ModelForm
from resto.models import Resto

class MoodEntryForm(ModelForm):
    class Meta:
        model = Resto
        fields = ['nama', 'makanan', 'lokasi']