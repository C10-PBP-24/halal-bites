from datetime import datetime
import json
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required

from authentication.models import CustomUser, UserProfile
from rating.models import Rating
from .models import Tracker, Food
from .forms import AddFoodTrackingForm
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.core.serializers import serialize
from food.models import Food
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


def show_json(request):
    # Use select_related to optimize query and fetch related Food objects
    data = Tracker.objects.select_related('food').all()

    # Serialize Tracker data with related Food information
    results = []
    for tracker in data:
        results.append({
            "model": "tracker.tracker",
            "pk": tracker.pk,
            "fields": {
                "user": str(tracker.user),  # Convert user to a string (username or ID)
                "food": {
                    "id": tracker.food.pk,
                    "name": tracker.food.name,
                    "price": tracker.food.price,
                    "promo": tracker.food.promo,
                },
                "order_at": tracker.order_at.strftime('%Y-%m-%d %H:%M:%S'),  # Format order_at
            }
        })

    # Return the custom JSON response
    return JsonResponse(results, safe=False)

@csrf_exempt
def add_tracker(request):
    if request.method == "POST":
        try:
            # Parse JSON data from request body
            data = json.loads(request.body)
            
            # Extract fields from the request
            food_id = data.get("food_id")
            order_at_str = data.get("order_at", None)  # May be a string

            # Validate that the food exists
            food = Food.objects.filter(pk=food_id).first()
            if not food:
                return JsonResponse({"error": "Food not found"}, status=404)

            # Parse the order_at field if it exists
            order_at = None
            if order_at_str:
                try:
                    # Convert string to datetime
                    order_at = datetime.strptime(order_at_str, '%Y-%m-%d %H:%M:%S')
                except ValueError:
                    return JsonResponse({"error": "Invalid datetime format for 'order_at'. Use 'YYYY-MM-DD HH:MM:SS'."}, status=400)

            # Create a new tracker entry
            tracker = Tracker.objects.create(
                user=request.user,
                food=food,
                order_at=order_at  # Pass parsed datetime or None
            )
            
            # Return success response
            return JsonResponse({
                "message": "Tracker created successfully",
                "tracker": {
                    "id": tracker.id,
                    "user": tracker.user.username,
                    "food_name": tracker.food.name,
                    "order_at": tracker.order_at.strftime('%Y-%m-%d %H:%M:%S') if tracker.order_at else None
                }
            }, status=201)
        
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    
    # Return error for unsupported methods
    return JsonResponse({"error": "Method not allowed"}, status=405)

@login_required
def food_tracker(request):
    user = request.user
    food_tracker = Tracker.objects.filter(user=user)
    rated_foods = Food.objects.filter(ratings__user=user).distinct()

    context = {
        'food_tracker': food_tracker,
        'rated_foods': rated_foods,
    }
    return render(request, 'tracker.html', context)


