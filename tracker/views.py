from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Tracker
from rating.models import Rating
from .forms import AddFoodTrackingForm

app_name = 'tracker'

def show_main(request):
    return render(request, 'main/main.html')

@login_required
def food_tracker(request):
    # Mengambil data tracking makanan user
    food_tracker = Tracker.objects.filter(user=request.user).select_related('restaurant', 'restaurant__makanan')
    
    # Including ratings for each food item in the tracker
    tracker_with_ratings = []
    for track in food_tracker:
        rating = Rating.objects.filter(food=track.restaurant.makanan, user=request.user).first()
        tracker_with_ratings.append({
            'tracker': track,
            'rating': rating.rating if rating else 'No rating',
        })
        
    return render(request, 'tracker.html', {
        'food_tracker': tracker_with_ratings,
    })

@login_required
def add_food_tracking(request):
    if request.method == 'POST':
        form = AddFoodTrackingForm(request.POST, user=request.user)
        if form.is_valid():
            food_tracking = form.save(commit=False)
            food_tracking.user = request.user
            food_tracking.save()
            return redirect('tracker:food_tracker')
    else:
        form = AddFoodTrackingForm(user=request.user)

    return render(request, 'foodtracker.html', {  # Ensure this template name matches your actual template file
        'form': form,
    })
