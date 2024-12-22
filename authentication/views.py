from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from authentication.forms import CustomUserCreationForm, CustomAuthenticationForm
from authentication.models import UserProfile
from django.contrib.auth import authenticate, login as auth_login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import logout as auth_logout
import json
from .models import CustomUser

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create a UserProfile for the new user
            UserProfile.objects.create(user=user)
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Redirect to a home page or dashboard
    else:
        form = CustomAuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')  # Redirect to a home page or login page

@csrf_exempt
def login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            auth_login(request, user)
            role = user.role
            # Status login sukses.
            return JsonResponse({
                "username": user.username,
                "role": role,
                "status": True,
                "message": "Login sukses!"
                # Tambahkan data lainnya jika ingin mengirim data ke Flutter.
            }, status=200)
        else:
            return JsonResponse({
                "status": False,
                "message": "Login gagal, akun dinonaktifkan."
            }, status=401)

    else:
        return JsonResponse({
            "status": False,
            "message": "Login gagal, periksa kembali email atau kata sandi."
        }, status=401)
    
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
from .models import CustomUser

@csrf_exempt
def register_flutter(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password1 = data.get('password1')
            password2 = data.get('password2')
            role = data.get('role')

            # Validasi data
            if not username or not password1 or not password2:
                return JsonResponse({
                    "status": False,
                    "message": "All fields are required."
                }, status=400)

            # Check if the passwords match
            if password1 != password2:
                return JsonResponse({
                    "status": False,
                    "message": "Passwords do not match."
                }, status=400)
            
            # Check if the username is already taken
            if CustomUser.objects.filter(username=username).exists():
                return JsonResponse({
                    "status": False,
                    "message": "Username already exists."
                }, status=400)
            
            # Create the new user
            user = CustomUser.objects.create_user(username=username, password=password1, role=role)
            user.save()
            
            return JsonResponse({
                "username": user.username,
                "role": user.role,
                "status": 'success',
                "message": "User created successfully!"
            }, status=201)

        except json.JSONDecodeError:
            return JsonResponse({
                "status": False,
                "message": "Invalid JSON format."
            }, status=400)

    else:
        return JsonResponse({
            "status": False,
            "message": "Invalid request method."
        }, status=405)

    
@csrf_exempt
def logout_flutter(request):
    username = request.user.username
    try:
        auth_logout(request)
        return JsonResponse({
            "username": username,
            "status": True,
            "message": "Logout berhasil!"
        }, status=200)
    except:
        return JsonResponse({
        "status": False,
        "message": "Logout gagal."
        }, status=401)