from django.shortcuts import render, redirect
from .forms import RatingForm

def show_rating_form(request):
    return render(request, "rating_form.html")

def create_rating(request):
    if request.method == 'POST':
        form = RatingForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('rating:show_rating_form')  # Replace 'some_view_name' with the name of the view you want to redirect to
    else:
        form = RatingForm()
    return render(request, 'rating_form.html', {'form': form})  # Replace 'template_name.html' with your template name