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
        if not request.user.is_authenticated:
            return JsonResponse({
                "status": False,
                "message": "User not authenticated."
            }, status=401)
        try:
            data = json.loads(request.body)
            food_id = data.get("food_id")
            rating_value = int(data.get("rating"))
            description = data.get("description", "")
            
            if not all([food_id, rating_value]):
                return JsonResponse({
                    "status": False,
                    "message": "Missing required fields."
                }, status=400)
            
            food = Food.objects.get(pk=food_id)
            new_rating = Rating.objects.create(
                user=request.user,
                rating=rating_value,
                description=description,
                food=food,
                created_at=datetime.now()
            )
            return JsonResponse({
                "status": "success",
                "message": "Review created successfully!"
            }, status=200)
        except Food.DoesNotExist:
            return JsonResponse({
                "status": False,
                "message": "Food not found."
            }, status=404)
        except Exception as e:
            return JsonResponse({
                "status": False,
                "message": f"Error creating review: {str(e)}"
            }, status=400)
    return JsonResponse({
        "status": False,
        "message": "Only POST method is allowed."
    }, status=405)