# views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Tracker, Food, Rating
from django.urls import reverse

@login_required
def food_tracker(request):
    user = request.user
    food_tracker = Tracker.objects.filter(user=user)
    rated_foods = Food.objects.filter(ratings__user=user).distinct()

    context = {
        'food_tracker': food_tracker,
        'rated_foods': rated_foods,
    }
    return render(request, 'tracker.html', context)

@login_required
def add_food_tracking(request):
    if request.method == 'POST':
        user = request.user
        food_id = request.POST.get('food')
        order_at = request.POST.get('order_at')
        food = Food.objects.get(id=food_id)
        Tracker.objects.create(user=user, food=food, order_at=order_at)
        return redirect(reverse('tracker:food_tracker'))

    return redirect(reverse('tracker:food_tracker'))