from django.urls import path
from . import views

urlpatterns = [
    path('./annotations/', views.annotation_list, name='annotation_list'),
    path('./', views.annot_menu, name='annot_menu'),
    path('./login/', views.login_view, name='login_view'),
    path('./inscription/', views.inscription, name = 'inscription'),
    path('./formulaire/', views.formulaire_genome, name = 'formulaire'),
    path('./annotateur_page/', views.annotateur_page, name='annotateur_page'),
]