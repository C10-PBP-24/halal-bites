from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers

from resto.models import Resto

# Create your views here.
def get_resto(request):
    data = Resto.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_resto(request):
    data = Resto.objects.all()
    return render(request, 'resto/main.html', {'restos': data})