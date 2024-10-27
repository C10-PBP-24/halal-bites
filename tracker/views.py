from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Tracker
from food.models import Food
from rating.models import Rating
from .forms import AddFoodTrackingForm

@login_required
def food_tracker(request):
    # Get the user's food tracking data
    food_tracker = Tracker.objects.filter(user=request.user)
    return render(request, 'tracker.html', {
        'food_tracker': food_tracker,
    })

@login_required
def add_food_tracking(request):
    if request.method == 'POST':
        form = AddFoodTrackingForm(request.POST)
        if form.is_valid():
            food_tracking = form.save(commit=False)
            food_tracking.user = request.user
            food_tracking.restaurant = food_tracking.food.resto  # Assuming each food has a related restaurant
            food_tracking.save()
            return redirect('tracker:food_tracker')
    else:
        ordered_foods = Food.objects.filter(ratings__user=request.user).distinct()
        user_ratings = Rating.objects.filter(user=request.user)
        form = AddFoodTrackingForm()

    # Print statements for debugging
    print("Ordered Foods:", ordered_foods)
    print("User Ratings:", user_ratings)

    return render(request, 'tracker.html', {
        'form': form,
        'ordered_foods': ordered_foods,
        'user_ratings': user_ratings
    })