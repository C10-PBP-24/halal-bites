from django.shortcuts import render, redirect
from .forms import RatingForm

def show_review(request):
    return render(request, "review.html")

def create_rating(request):
    if request.method == 'POST':
        form = RatingForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('rating:show_review')  # Replace 'some_view_name' with the name of the view you want to redirect to
    else:
        form = RatingForm()
    return render(request, 'review.html', {'form': form})  # Replace 'template_name.html' with your template name