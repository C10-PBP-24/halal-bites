from django.urls import path
from .views import ThreadListView, ThreadDetailView, CreateThreadView, CreatePostView, add_post, create_post_ajax, delete_thread, delete_post, create_thread_ajax, edit_thread, edit_post, thread_list,show_json, show_post_json, create_post_flutter, edit_post_flutter, edit_thread_flutter, delete_post_flutter, delete_thread_flutter

app_name = 'forum'

urlpatterns = [
    path('', ThreadListView.as_view(), name='thread_list'),
    path('<int:pk>/', ThreadDetailView.as_view(), name='thread_detail'),
    path('create/', CreateThreadView.as_view(), name='create_thread'),
    path('<int:pk>/create_post/', CreatePostView.as_view(), name='create_post'),
    path('add_post/', add_post, name='add_post'),  # Endpoint for adding posts via API
    path('create_post_ajax/<int:thread_id>/', create_post_ajax, name='create_post_ajax'),
    path('<int:pk>/delete_thread/', delete_thread, name='delete_thread'),
    path('<int:pk>/delete_post/', delete_post, name='delete_post'),
    path('create_thread_ajax/', create_thread_ajax, name='create_thread_ajax'),
    # New routes for thread management
    path('threads/<int:thread_id>/edit/', edit_thread, name='edit_thread'),
    path('threads/<int:thread_id>/delete/', delete_thread, name='delete_thread'),

    # New routes for post management
    path('posts/<int:post_id>/edit/', edit_post, name='edit_post'),
    path('posts/<int:post_id>/delete/', delete_post, name='delete_post'),\
    path('threads/', thread_list, name='thread_list'),
    path('threads/json/', show_json, name='show_json'),
    path('threads/<int:thread_id>/json/', show_post_json, name='show_post_json'),

    path('create-post-flutter/', create_post_flutter, name='create_post_flutter'),
    path('edit-post-flutter/<int:post_id>/', edit_post_flutter, name='edit_post_flutter'),
    path('edit-thread-flutter/<int:thread_id>/', edit_thread_flutter, name='edit_thread_flutter'),
    path('delete-post-flutter/<int:post_id>/', delete_post_flutter, name='delete_post_flutter'),
    path('delete-thread-flutter/<int:thread_id>/', delete_thread_flutter, name='delete_thread_flutter'),
]

