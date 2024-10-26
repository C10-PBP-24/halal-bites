from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse, HttpResponseNotFound, HttpResponseRedirect
from .models import Thread, Post
from .forms import ThreadForm, PostForm  # Assuming you have forms for creating threads and posts
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.utils.html import strip_tags
from django.views.decorators.http import require_POST

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
    user = request.user

    # Create a new thread
    new_thread = Thread(title=title, user=user)
    new_thread.save()

    return JsonResponse({
        "status": "success",
        "message": "Thread created successfully",
        "thread_id": new_thread.id
    }, status=201)


@csrf_exempt
@require_POST
def create_post_ajax(request, pk):
    # Get the thread based on its pk
    thread = get_object_or_404(Thread, pk=pk)

    # Extract form data from the request
    content = strip_tags(request.POST.get("content"))
    user = request.user  # Get the current user

    # Create a new post
    new_post = Post(thread=thread, content=content,)# user=user)
    new_post.save()

    # Return a JSON response indicating success
    return JsonResponse({
        "status": "success",
        "message": "Post created successfully",
        "post_id": new_post.id,
        "thread_id": thread.id
    }, status=201)

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

def delete_thread(request, pk):
    thread = get_object_or_404(Thread, pk=pk)
    if request.user == thread.user:  # Ensure that only the owner can delete the thread
        thread.delete()
        return HttpResponseRedirect(reverse('forum:thread_list'))  # Redirect to the thread list
    else:
        return HttpResponse(status=403)  # Forbidden if the user is not the owner


def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    thread_id = post.thread.id  # Get the thread ID before deleting the post
    if request.user == post.user:  # Ensure that only the owner can delete the post
        post.delete()
        return HttpResponseRedirect(reverse('forum:thread_detail', kwargs={'pk': thread_id}))  # Redirect to the thread
    else:
        return HttpResponse(status=403)  # Forbidden if the user is not the owner


