from django.urls import path

from . import views

urlpatterns = [
    path('show_memory', views.show_memory, name='TTMemory'),
    path('fetch_memory', views.fetch_memory, name='TTMemory'),
]
