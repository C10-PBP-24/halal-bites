from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.core import serializers
from .models import Food
from django.contrib.auth.decorators import login_required
from authentication.models import UserProfile


@login_required(login_url="authentication:login")
def show_food(request):
    user = request.user
    user_profile = UserProfile.objects.get(user=user)

    foods = Food.objects.all()

    context = {
        'products' : foods
    }

    return render(request, 'menu.html', context)

@login_required(login_url="authentication:login")
def food_detail(requets, food_id):
    food = get_object_or_404(Food, food_id)
    context = {'food': food}
    return render(requets, 'food_detail.html', context)

def get_food(request):
    data = Food.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")


def get_food_by_id(request, id):
    data = Food.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")
