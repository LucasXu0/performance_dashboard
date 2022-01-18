from django.urls import path

from . import views

urlpatterns = [
    path('show_memory', views.show_memory, name='TTMemory'),
    path('fetch_memory', views.fetch_memory, name='TTMemory'),
    path('index', views.index, name='TTMemory'),
    path('upload_performance_json', views.upload_performance_json, name='TTMemory'),
]

