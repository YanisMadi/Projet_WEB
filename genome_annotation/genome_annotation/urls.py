from django.contrib import admin
from django.urls import path, include
from genome import urls
from genome import views

urlpatterns = [
    path('admin/', admin.site.urls, name="admin"),
    path('annotations/', views.annotation_list, name='annotation_list'),
    path('', views.annot_menu, name='annot_menu'),
    path('login/', views.login_view, name='login_view'),
    path('inscription/', views.inscription, name = 'inscription'),
    path('formulaire/', views.formulaire_genome, name = 'formulaire'),
    path('annotateur_page/', views.annotateur_page, name='annotateur_page'),
    path('validateur_page/', views.validateur_page, name='validateur_page'),
    path('lecteur_page/', views.lecteur_page, name='lecteur_page'),
    path('logout/', views.logout_view, name='logout'),
    path('manage_users/', views.manage_users, name='manage_users'),
    path('sequence/', views.show_sequences, name='sequence'),
    path('validation/', views.validate_annotation, name='validation'),
    path('assign_annotation/', views.assign_annotation, name = 'assign_annotation'),
]
