from django.urls import path
from . import views

urlpatterns = [
    path('annotations/', views.annotation_list, name='annotation_list'),
    path('menu/', views.annot_menu, name='annot_menu'),
]
