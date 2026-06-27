from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('edit/', views.edit_profile_view, name='edit_profile'),
    path('search/', views.search_view, name='search'),
    path('follow/<str:username>/', views.follow_toggle, name='follow_toggle'),
    path('<str:username>/', views.profile_view, name='profile'),
    path('<str:username>/followers/', views.followers_view, name='followers'),
    path('<str:username>/following/', views.following_view, name='following'),
]
