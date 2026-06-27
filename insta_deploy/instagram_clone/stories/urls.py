from django.urls import path
from . import views

app_name = 'stories'

urlpatterns = [
    path('create/', views.create_story_view, name='create'),
    path('delete/<int:story_id>/', views.delete_story, name='delete'),
    path('<str:username>/', views.view_story, name='view'),
]
