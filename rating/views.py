from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import RatingForm
from .models import Food

def show_rating_form(request):
    return render(request, "rating_form.html")

@login_required
def create_rating(request, food_id):
    food = get_object_or_404(Food, id=food_id)
    
    if request.method == 'POST':
        form = RatingForm(request.POST, request.FILES)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.food = food
            rating.user = request.user
            rating.save()
            return redirect('rating:show_rating_form')  # Replace 'rating:show_rating_form' with the name of the view you want to redirect to
    else:
        form = RatingForm()
    
    return render(request, 'rating_form.html', {'form': form, 'food': food})  # Replace 'rating_form.html' with your template name