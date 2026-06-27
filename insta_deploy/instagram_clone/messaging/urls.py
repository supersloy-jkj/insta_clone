from django.urls import path
from . import views

app_name = 'messaging'

urlpatterns = [
    path('', views.inbox_view, name='inbox'),
    path('new/<str:username>/', views.new_conversation, name='new_conversation'),
    path('<int:conv_id>/', views.conversation_view, name='conversation'),
    path('<int:conv_id>/poll/', views.poll_messages, name='poll_messages'),
]
