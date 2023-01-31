"""genome_annotation URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from genome import views

urlpatterns = [
    path('admin/', admin.site.urls),
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
]
