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
from django.middleware.csrf import get_token


from resto.models import Resto

def get_resto(request):
    data = Resto.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

@login_required(login_url='auth/login')
def show_resto(request):
    data = Resto.objects.all()
    user = request.user
    if(user.role=="user"):
        return render(request, 'resto/resto_user.html', {'restos': data})
    else:
        return render(request, 'resto/resto_admin.html', {'restos': data})

        

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
        filtered_restos = Resto.objects.filter(lokasi__icontains=lokasi)  # Filter by location
    if nama:
        filtered_restos = filtered_restos.filter(nama__icontains=nama)  # Filter by name

    data = [
        {
            'pk': resto.pk,
            'nama': resto.nama,
            'lokasi': resto.lokasi
        }
        for resto in filtered_restos
    ]
    
    return JsonResponse({'restos': data})

@csrf_exempt 
@require_POST
def add_resto(request):
    nama = strip_tags(request.POST.get("nama"))
    nama_makanan = strip_tags(request.POST.get("nama_makanan"))
    harga_makanan = strip_tags(request.POST.get("harga_makanan"))
    promo_makanan = strip_tags(request.POST.get("promo_makanan"))
    image_makanan = strip_tags(request.POST.get("image_makanan"))
    lokasi = strip_tags(request.POST.get("lokasi"))

    # Create the Food object
    new_food = Food(name=nama_makanan, price=harga_makanan, image=image_makanan, promo=promo_makanan)
    new_food.save()

    # Create the Resto object with the new Food's ID
    new_resto = Resto(nama=nama, makanan=new_food, lokasi=lokasi)
    new_resto.save()

    return HttpResponse(b"CREATED", status=201)

@csrf_exempt
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

@csrf_exempt
def create_resto_flutter(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        required_fields = ["name", "name_makanan", "price", "image", "promo", "lokasi"]
        for field in required_fields:
            if not data.get(field):
                return JsonResponse({"status": "error", "message": f"Missing field: {field}"}, status=400)

        new_food = Food.objects.create(
            name=data["name_makanan"],
            price=data["price"],
            image=data["image"],
            promo=data["promo"],
        )
        new_food.save()
        new_resto = Resto.objects.create(
            nama=data["name"],
            makanan=new_food,
            lokasi=data["lokasi"],
        )
        new_resto.save()
        return JsonResponse({"status": "success"}, status=200)
    else:
        return JsonResponse({"status": "error"}, status=401)
    
@csrf_exempt
def edit_resto_flutter(request, id):
    try:
        resto = Resto.objects.get(pk=id)
    except Resto.DoesNotExist:
        return JsonResponse({"status": "error", "message": "Restaurant not found"}, status=404)

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            resto.nama = data.get("nama", resto.nama)
            resto.lokasi = data.get("lokasi", resto.lokasi)
            resto.save()
            return JsonResponse({"status": "success"}, status=200)
        except (KeyError, ValueError) as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)
    else:
        return JsonResponse({"status": "error", "message": "Invalid request method"}, status=401)

def get_csrf_token(request):
    csrf_token = get_token(request)
    return JsonResponse({"status": "success", "csrfToken": csrf_token})
