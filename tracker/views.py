from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from .models import Tracker, Food, Rating
from .forms import AddFoodTrackingForm

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
        form = AddFoodTrackingForm(request.POST, user=request.user)
        if form.is_valid():
            food = form.cleaned_data['food']
            order_at = form.cleaned_data['order_at']
            rating = Rating.objects.get(user=request.user, food=food)
            Tracker.objects.create(user=request.user, food=food, order_at=order_at, rating=rating)
            return redirect(reverse('tracker:food_tracker'))

    return redirect(reverse('tracker:food_tracker'))
