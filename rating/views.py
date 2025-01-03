from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import RatingForm
from food.models import Food
from django.http import JsonResponse, HttpResponse
from django.core import serializers
from .models import Rating
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
from datetime import datetime
from django.contrib import messages
from django.db import IntegrityError
from django.views.decorators.http import require_POST, require_GET
from django.db.models import Avg, Q

@login_required
def create_rating(request, food_id):
    food = get_object_or_404(Food, id=food_id)
    
    if request.method == 'POST':
        existing_rating = Rating.objects.filter(user=request.user, food=food).first()
        if existing_rating:
            messages.error(request, "You have already reviewed this food.")
            return redirect('rating:rated_foods')
        form = RatingForm(request.POST)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.food = food
            rating.user = request.user
            rating.save()
            return redirect('rating:rated_foods')
    else:
        form = RatingForm()
    
    return render(request, 'rating_form.html', {'form': form, 'food': food})

@login_required
def edit_rating(request, rating_id):
    rating = get_object_or_404(Rating, id=rating_id, user=request.user)
    if request.method == 'POST':
        form = RatingForm(request.POST, instance=rating)
        if form.is_valid():
            form.save()
            return redirect('rating:rated_foods')
    else:
        form = RatingForm(instance=rating)
    return render(request, 'rating_edit_form.html', {'form': form, 'food': rating.food})

@login_required
def delete_rating(request, rating_id):
    rating = get_object_or_404(Rating, id=rating_id, user=request.user)
    if request.method == 'POST':
        rating.delete()
        return redirect('rating:rated_foods')
    return render(request, 'rating_delete_confirm.html', {'rating': rating})

@login_required
def rated_foods(request):
    # Start with all foods that have at least one rating
    foods = Food.objects.filter(ratings__isnull=False).annotate(average_rating=Avg('ratings__rating')).distinct()
    
    rating_filter = request.GET.get('rating', '').strip()
    user_filter = request.GET.get('user_filter', '').strip()

    # Handle rating filter
    if rating_filter in ['1', '2', '3', '4', '5']:
        min_rating = int(rating_filter)
        max_rating = min_rating + 1
        if min_rating < 5:
            foods = foods.filter(
                average_rating__gte=min_rating,
                average_rating__lt=max_rating
            )
        else:
            # rating_filter == '5'
            foods = foods.filter(
                average_rating__gte=min_rating
            )

    # Handle user-specific filter
    if user_filter == 'my_reviews':
        foods = foods.filter(ratings__user=request.user)
    
    # Attach the user's own rating to each Food if it exists
    for f in foods:
        user_rating = f.ratings.filter(user=request.user).first()
        f.user_rating = user_rating
    
    context = {
        'foods': foods,
        'rating_filter': rating_filter,  # Added
        'user_filter': user_filter,      # Added
    }
    return render(request, 'rated_foods.html', context)


def show_xml(request):
    data = Rating.objects.all()
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json(request):
    data = list(Rating.objects.values(
        'id',
        'food_id',
        'food__name',
        'user_id',
        'user__username',
        'rating',
        'description',
        'created_at'
    ))
    return JsonResponse(data, safe=False)

@csrf_exempt
def create_rating_flutter(request):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return JsonResponse({
                "status": False,
                "message": "User not authenticated."
            }, status=401)
        try:
            data = json.loads(request.body)
            food_id = data.get("food_id")
            rating_value = int(data.get("rating"))
            description = data.get("description", "")
            
            if not all([food_id, rating_value]):
                return JsonResponse({
                    "status": False,
                    "message": "Missing required fields."
                }, status=400)
            
            food = Food.objects.get(pk=food_id)
            
            # Check for existing rating
            existing_rating = Rating.objects.filter(user=request.user, food=food).first()
            if existing_rating:
                return JsonResponse({
                    "status": False,
                    "message": "You have already reviewed this food."
                }, status=400)
            
            new_rating = Rating.objects.create(
                user=request.user,
                rating=rating_value,
                description=description,
                food=food,
                created_at=datetime.now()
            )
            return JsonResponse({
                "status": "success",
                "message": "Review created successfully!"
            }, status=200)
        except Food.DoesNotExist:
            return JsonResponse({
                "status": False,
                "message": "Food not found."
            }, status=404)
        except IntegrityError:
            return JsonResponse({
                "status": False,
                "message": "You have already reviewed this food."
            }, status=400)
        except Exception as e:
            return JsonResponse({
                "status": False,
                "message": f"Error creating review: {str(e)}"
            }, status=400)
    return JsonResponse({
        "status": False,
        "message": "Only POST method is allowed."
    }, status=405)

@csrf_exempt
def edit_rating_flutter(request, rating_id):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return JsonResponse({
                "status": False,
                "message": "User not authenticated."
            }, status=401)
        try:
            rating = Rating.objects.get(pk=rating_id, user=request.user)
            data = json.loads(request.body)
            rating_value = int(data.get("rating"))
            description = data.get("description", "")
            
            rating.rating = rating_value
            rating.description = description
            rating.save()
            
            return JsonResponse({
                "status": "success",
                "message": "Review updated successfully!"
            }, status=200)
        except Rating.DoesNotExist:
            return JsonResponse({
                "status": False,
                "message": "Rating not found."
            }, status=404)
        except Exception as e:
            return JsonResponse({
                "status": False,
                "message": f"Error updating review: {str(e)}"
            }, status=400)
    return JsonResponse({
        "status": False,
        "message": "Only POST method is allowed."
    }, status=405)

@csrf_exempt
def delete_rating_flutter(request, rating_id):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return JsonResponse({
                "status": False,
                "message": "User not authenticated."
            }, status=401)
        try:
            rating = Rating.objects.get(pk=rating_id, user=request.user)
            rating.delete()
            return JsonResponse({
                "status": "success",
                "message": "Review deleted successfully!"
            }, status=200)
        except Rating.DoesNotExist:
            return JsonResponse({
                "status": False,
                "message": "Rating not found."
            }, status=404)
        except Exception as e:
            return JsonResponse({
                "status": False,
                "message": f"Error deleting review: {str(e)}"
            }, status=400)
    return JsonResponse({
        "status": False,
        "message": "Only POST method is allowed."
    }, status=405)

@login_required
@require_GET
def get_rating_ajax(request, rating_id):
    try:
        rating = Rating.objects.get(pk=rating_id, user=request.user)
        data = {
            "id": str(rating.id),
            "rating": rating.rating,
            "description": rating.description,
        }
        return JsonResponse({"success": True, "data": data})
    except Rating.DoesNotExist:
        return JsonResponse({"success": False, "error": "Rating not found"}, status=404)

@csrf_exempt
@login_required
@require_POST
def edit_rating_ajax(request):
    try:
        req_data = json.loads(request.body)
        rating_id = req_data.get("rating_id")
        rating_value = req_data.get("rating")
        description = req_data.get("description", "")
        rating_obj = Rating.objects.get(pk=rating_id, user=request.user)
        rating_obj.rating = rating_value
        rating_obj.description = description
        rating_obj.save()
        return JsonResponse({"success": True, "message": "Rating updated successfully"})
    except Rating.DoesNotExist:
        return JsonResponse({"success": False, "error": "Rating not found"}, status=404)
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=400)

@csrf_exempt
@login_required
@require_POST
def delete_rating_ajax(request):
    try:
        req_data = json.loads(request.body)
        rating_id = req_data.get("rating_id")
        rating_obj = Rating.objects.get(pk=rating_id, user=request.user)
        rating_obj.delete()
        return JsonResponse({"success": True, "message": "Rating deleted successfully"})
    except Rating.DoesNotExist:
        return JsonResponse({"success": False, "error": "Rating not found"}, status=404)
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=400)