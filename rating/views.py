from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import RatingForm
from food.models import Food
from django.http import JsonResponse, HttpResponse
from django.core import serializers
from .models import Rating

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