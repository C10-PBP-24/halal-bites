from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Tracker, Food, Rating
from .forms import AddFoodTrackingForm

app_name = 'tracker'

def show_main(request):
    return render(request, 'main/main.html')

@login_required
def food_tracker(request):
    # Mengambil data tracking makanan user
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
            food_tracking.save()
            return redirect('tracker:food_tracker')
    else:
        form = AddFoodTrackingForm()

    return render(request, 'foodtracker.html', {
        'form': form,
    })
