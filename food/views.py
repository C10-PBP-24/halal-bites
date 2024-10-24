from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.core import serializers
from .models import Food
from django.contrib.auth.decorators import login_required


@login_required
def show_food(request):

    return(request)

def get_foods(request):
    data = Food.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json" )


