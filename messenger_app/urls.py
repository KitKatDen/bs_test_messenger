from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home_mes'),
    path('view_chat/<int:pk>/', view_chat, name='view_chat'),
    path('view_chat/', view_chat, name='view_chat'),
    path('write_msg/', write_msg, name='write_msg'),
]