from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse, HttpResponseNotFound, HttpResponseRedirect
from .models import Thread, Post, Food  # Pastikan untuk mengimpor model Food
from .forms import ThreadForm, PostForm  # Assuming you have forms for creating threads and posts
import json
from django.views.decorators.csrf import csrf_exempt
from django.utils.html import strip_tags
from django.views.decorators.http import require_POST
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Thread, Post
from django.core.serializers import serialize
from food.models import Food

def show_post_json(request, thread_id):
    thread = get_object_or_404(Thread, id=thread_id)
    posts = Post.objects.filter(thread=thread)
    return HttpResponse(serialize("json", posts), content_type="application/json")

def show_json(request):
    data = Thread.objects.all()
    return HttpResponse(serialize("json", data), content_type="application/json")


# def show_json(request, thread_id):
#     # Fetch the thread by its ID, or return a 404 error if it does not exist
#     thread = get_object_or_404(Thread, id=thread_id)
    
#     # Serialize the thread data
#     thread_data = {
#         'id': thread.id,
#         'title': thread.title,
#         'created_at': thread.created_at,
#         'user': thread.user.username,  # Assuming the user has a 'username' attribute
#         'foods': [food.name for food in thread.foods.all()],  # Assuming Food model has a 'name' attribute
#     }
    
#     # Fetch the posts related to the thread
#     posts = Post.objects.filter(thread=thread)
#     posts_data = []
    
#     for post in posts:
#         posts_data.append({
#             'id': post.id,
#             'content': post.content,
#             'created_at': post.created_at,
#             'user': post.user.username,  # Assuming the user has a 'username' attribute
#         })
    
#     # Combine the thread data and posts data into one response
#     response_data = {
#         'thread': thread_data,
#         'posts': posts_data,
#     }
    
#     return JsonResponse(response_data)

# List all threads
class ThreadListView(ListView):
    model = Thread
    template_name = 'forum/thread_list.html'
    context_object_name = 'threads'

# View details of a specific thread and its posts
class ThreadDetailView(DetailView):
    model = Thread
    template_name = 'forum/thread_detail.html'
    context_object_name = 'thread'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.filter(thread=self.object)
        context['foods'] = Food.objects.filter(thread=self.object)  # Menampilkan makanan yang terkait dengan thread
        return context

# Create a new thread (similar to asking a question)
class CreateThreadView(CreateView):
    model = Thread
    form_class = ThreadForm
    template_name = 'forum/create_thread.html'
    success_url = reverse_lazy('forum:thread_list')  # Redirect to thread list after creation

    def form_valid(self, form):
        form.instance.user = self.request.user  # Associate the thread with the current user
        return super().form_valid(form)

# Create a new post (similar to answering a question)
class CreatePostView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'forum/create_post.html'

    def form_valid(self, form):
        # Get the thread object based on the thread's primary key (pk) from the URL
        thread = get_object_or_404(Thread, pk=self.kwargs['pk'])
        form.instance.thread = thread  # Associate the post with the thread
        form.instance.user = self.request.user  # Associate the post with the current user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        # Pass the thread object to the template context
        context = super().get_context_data(**kwargs)
        context['thread'] = get_object_or_404(Thread, pk=self.kwargs['pk'])
        return context

    def get_success_url(self):
        # Redirect to the thread detail page after creating the post
        return reverse_lazy('forum:thread_detail', kwargs={'pk': self.kwargs['pk']})

@csrf_exempt
@require_POST
def create_thread_ajax(request):
    title = strip_tags(request.POST.get("title"))
    food_name = strip_tags(request.POST.get("food"))  # Ambil nama makanan dari request

    # Buat thread baru
    new_thread = Thread(title=title, user=request.user)
    new_thread.save()

    # Simpan makanan yang terkait dengan thread jika ada
    if food_name:  # Cek jika food_name tidak kosong
        foods = Food.objects.filter(name=food_name)  # Ambil semua objek Food berdasarkan nama
        if foods.exists():
            food = foods.first()  # Ambil objek pertama
            new_thread.foods.add(food)  # Pastikan ini sesuai dengan relasi di model

    return JsonResponse({
        "status": "success",
        "message": "Thread created successfully",
        "thread_id": new_thread.id
    }, status=201)

@csrf_exempt
def create_post_ajax(request, thread_id):
    if request.method == 'POST':
        post_content = request.POST.get('content')
        user = request.user

        if not post_content:
            return JsonResponse({"status": "Content cannot be empty"}, status=400)

        thread = get_object_or_404(Thread, id=thread_id)
        new_post = Post(thread=thread, content=post_content, user=user)
        new_post.save()

        return JsonResponse({"status": "Post added", "post_id": new_post.id}, status=201)
    return JsonResponse({"status": "Invalid request"}, status=400)


# CSRF-exempt API for adding posts via AJAX or mobile
@csrf_exempt
def add_post(request):
    if request.method == "POST":
        data = json.loads(request.body)
        thread = Thread.objects.get(pk=data.get('thread_id'))
        post_content = data.get('content')
        user = request.user

        # Create a new post
        new_post = Post(thread=thread, content=post_content, user=user)
        new_post.save()

        return JsonResponse({"status": "Post added", "post_id": new_post.id}, status=201)
    return JsonResponse({"status": "Invalid request"}, status=400)

@login_required
def edit_thread(request, thread_id):
    thread = get_object_or_404(Thread, id=thread_id, user=request.user)

    if request.method == "POST":
        thread.title = request.POST.get('title')
        thread.save()
        return redirect('forum:thread_list')  # Mengarahkan kembali ke daftar thread setelah penyimpanan

    context = {
        'thread': thread
    }
    return render(request, 'forum/thread_list.html', context)  # Mengarahkan kembali ke thread_list.html

@login_required
def delete_thread(request, thread_id):
    thread = get_object_or_404(Thread, id=thread_id, user=request.user)
    thread.delete()
    return redirect('forum:thread_list')

@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, user=request.user)

    if request.method == "POST":
        post.content = request.POST.get('content')
        post.save()
        return redirect('forum:thread_detail', pk=post.thread.id)  # Redirect to thread detail page

    context = {
        'post': post
    }
    return redirect('forum:thread_detail', pk=post.thread.id)

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, user=request.user)
    post.delete()
    return redirect('forum:thread_detail', pk=post.thread.id)

@login_required
def thread_list(request):
    query = request.GET.get('q')  # Get the search term from the query string
    if query:
        threads = Thread.objects.filter(Q(title__icontains=query))
    else:
        threads = Thread.objects.all()

    # Ambil semua makanan untuk dropdown
    foods = Food.objects.all()

    context = {
        'threads': threads,
        'foods': foods,  # Tambahkan foods ke dalam konteks
    }
    return render(request, 'forum/thread_list.html', context)
