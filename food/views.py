from django.http import HttpResponse, HttpResponseNotFound, JsonResponse, HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from django.core import serializers
from food.models import Food
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from authentication.models import UserProfile
from django.views.decorators.csrf import csrf_exempt
from rating.forms import RatingForm
from food.form import FoodEntryForm


@login_required(login_url="authentication:login")
def show_menu(request):
    user = request.user

    if user.role.casefold() == "admin":
        food_list = serializers.serialize('json', Food.objects.all())
        food_list = serializers.deserialize('json', food_list)
        food_list = [food.object for food in food_list]

        return render(request, 'menu_owner.html', {'foods': food_list})
    foods = Food.objects.all()
    context = {
        'foods' : foods
    }
    return render(request, 'menu.html', context)

@login_required(login_url="authentication:login")
def food_detail(request, food_id):
    food = get_object_or_404(Food, id=food_id)
    ratings = food.ratings.all()
    average_rating = food.get_average_rating()

    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.food = food
            rating.user = request.user
            rating.save()
            return redirect('food:food_detail', food_id=food.id)
    else:
        form = RatingForm()

    context = {
        'food': food,
        'ratings': ratings,
        'average_rating': average_rating,
        'form': form,
    }
    return render(request, 'food_detail.html', context)

@csrf_exempt
def add_food(request, instance):
    form = FoodEntryForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        food = form.save(commit=False)
        food.user =request.user
        food.save()
        return redirect('main:show_menu')

    context = {'form': form}
    return render(request, "add_food.html", context)

def get_food(request):
    data = Food.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def get_food_by_id(request, id):
    data = Food.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

@csrf_exempt
def filter_food(request):
    price = request.GET.get('price')
    foods = Food.objects.filter(price__lte=price)
    data = []
    for food in foods:
        data.append({
            'id': food.id,
            'name': food.name,
            'price': food.price,
            'promo': food.promo,
            'image': food.image,
            'average_rating': food.get_average_rating(),
        })
    return JsonResponse(data, safe=False)

def edit_product(request, id):
    food = Food.objects.get(pk = id)
    form = add_food(request.POST or None, instance=food)

    if form.is_valid() and request.method == "POST":
        form.save()
        return HttpResponseRedirect(reverse('food:show_menu'))

    context = {'form': form}
    return render(request, "edit_food.html", context)

def delete_product(request, id):
    food = Food.objects.get(pk = id)
    food.delete()
    return HttpResponseRedirect(reverse('food:show_menu'))

