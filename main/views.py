from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def show_main(request):
    return render(request, 'main.html')
