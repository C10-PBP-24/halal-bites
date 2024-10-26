from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.core import serializers
import json
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.utils.html import strip_tags
from food.models import Food
from django.http import HttpResponseRedirect


from resto.models import Resto

# Create your views here.
def get_resto(request):
    data = Resto.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

@login_required(login_url='auth/login')
def show_resto(request):
    data = Resto.objects.all()
    return render(request, 'resto/resto.html', {'restos': data})

def resto_detail(request, pk):
    resto = get_object_or_404(Resto, pk=pk)
    food = get_object_or_404(Food, pk=pk)
    context = {
        "resto":resto,
    }
    return render(request, 'resto/resto_detail.html', context)
    

def filter_resto(request):
    lokasi = request.GET.get('lokasi', None)  # Get the location parameter from the request
    nama = request.GET.get('nama', None)  # Get the name parameter from the request

    filtered_restos = Resto.objects.all()
    if lokasi:
        filtered_restos = Resto.objects.filter(lokasi__icontains=lokasi)  # Filter by location (case-insensitive)
    if nama:
        filtered_restos = filtered_restos.filter(nama__icontains=nama)  # Filter by location (case-insensitive)

    data = [
        {
            'pk': resto.pk,      # Include the primary key
            'nama': resto.nama,
            'lokasi': resto.lokasi
        }
        for resto in filtered_restos
    ]
    
    return JsonResponse({'restos': data})  # Use JsonResponse to return the data

@csrf_exempt 
@require_POST
def add_resto(request):
    nama = strip_tags(request.POST.get("nama"))
    print("nama "+ nama)
    nama_makanan = strip_tags(request.POST.get("nama_makanan"))
    harga_makanan = strip_tags(request.POST.get("harga_makanan"))
    promo_makanan = strip_tags(request.POST.get("promo_makanan"))
    image_makanan = strip_tags(request.POST.get("image_makanan"))
    lokasi = strip_tags(request.POST.get("lokasi"))

    # Create the Food object first
    new_food = Food(name=nama_makanan, price=harga_makanan, image=image_makanan, promo=promo_makanan)
    new_food.save()

    # Now create the Resto object with the new Food's ID
    new_resto = Resto(nama=nama, makanan=new_food, lokasi=lokasi)
    new_resto.save()

    return HttpResponse(b"CREATED", status=201)

def delete_resto(request, id):
    resto = Resto.objects.get(pk=id)
    resto.delete()
    return HttpResponse(status=204)

def show_xml(request):
    data = Resto.objects.all()
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json(request):
    data = Resto.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")