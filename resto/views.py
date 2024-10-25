from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core import serializers

from resto.models import Resto

# Create your views here.
def get_resto(request):
    data = Resto.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_resto(request):
    data = Resto.objects.all()
    return render(request, 'resto/main.html', {'restos': data})

def filter_resto(request):
    lokasi = request.GET.get('lokasi', None)  # Get the location parameter from the request
    if lokasi:
        filtered_restos = Resto.objects.filter(lokasi__icontains=lokasi)  # Filter by location (case-insensitive)
    else:
        filtered_restos = Resto.objects.all()  # If no location, return all restaurants

    data = [
        {'nama': resto.nama, 'lokasi': resto.lokasi}
        for resto in filtered_restos
    ]
    return JsonResponse({'restos': data})