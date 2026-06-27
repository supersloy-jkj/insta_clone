from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.feed_view, name='feed'),
    path('create/', views.create_post_view, name='create_post'),
    path('saved/', views.saved_posts_view, name='saved_posts'),
    path('post/<int:post_id>/', views.post_detail_view, name='post_detail'),
    path('post/<int:post_id>/delete/', views.delete_post_view, name='delete_post'),
    path('post/<int:post_id>/like/', views.like_toggle, name='like_toggle'),
    path('post/<int:post_id>/save/', views.save_toggle, name='save_toggle'),
]
