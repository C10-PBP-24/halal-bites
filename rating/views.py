from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import RatingForm
from food.models import Food
from django.http import JsonResponse, HttpResponse
from django.core import serializers
from .models import Rating
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
from datetime import datetime

@login_required
def create_rating(request, food_id):
    food = get_object_or_404(Food, id=food_id)
    
    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.food = food
            rating.user = request.user
            rating.save()
            return redirect('rating:rated_foods')
    else:
        form = RatingForm()
    
    return render(request, 'rating_form.html', {'form': form, 'food': food})

def rated_foods(request):
    foods = Food.objects.filter(ratings__isnull=False).distinct()
    context = {
        'foods': foods,
    }
    return render(request, 'rated_foods.html', context)

def show_xml(request):
    data = Rating.objects.all()
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json(request):
    data = list(Rating.objects.values(
        'id',
        'food_id',
        'food__name',
        'user_id',
        'user__username',
        'rating',
        'description',
        'created_at'
    ))
    return JsonResponse(data, safe=False)

@csrf_exempt
def create_rating_flutter(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        new_rating = Rating.objects.create(
            user=request.user,
            rating=int(data["rating"]),
            description=data["description"],
            food_id=data["food_id"],
            created_at=datetime.now()
        )
        new_rating.save()
        return JsonResponse({"status": "success"}, status=200)
    else:
        return JsonResponse({"status": "error"}, status=401)