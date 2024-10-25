from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.core import serializers
from food.models import Food
from django.contrib.auth.decorators import login_required
# from authentication.models import UserProfile
from django.views.decorators.csrf import csrf_exempt


@login_required(login_url="authentication:login")
def show_menu(request):
    # user = request.user
    # user_profile = UserProfile.objects.get(user=user)

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

@csrf_exempt
def add_food(request):
    if request.method == "POST":
        name = request.POST.get('Name')
        price = request.POST.get('Price')
        image = request.POST.get('Image')
        promo = request.POST.get('Promo')

        new_food = Food(name=name, price=price, image=image, promo=promo)
        new_food.save()
        return HttpResponse(b"CREATED", status=201)
    return HttpResponseNotFound()

def get_food(request):
    data = Food.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")


def get_food_by_id(request, id):
    data = Food.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

@csrf_exempt
def filter_food(request):
    price = request.GET.get('price', '')

    foods = Food.objects.all()
    if price:
        foods = foods.filter(price__icontains=price)

    foods_json = serializers.serialize('json', foods)
    return JsonResponse(foods_json, safe=False)

