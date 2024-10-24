from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers

from models import Resto

# Create your views here.
def get_resto(request):
    data = Resto.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")