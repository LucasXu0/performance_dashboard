from django.urls import path

from . import views

urlpatterns = [
    path('bar', views.ChartViewGet, name='TTMemory'),
    path('index', views.IndexViewGet, name='TTMemory'),
    # path('', views.index, name='index'),
]
