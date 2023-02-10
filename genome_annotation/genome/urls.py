from django.urls import path
from . import views
from django.contrib.auth.decorators import user_passes_test
from django.urls import re_path



urlpatterns = [
    path('annotations/', views.annotation_list, name='annotation_list'),
    path('', views.annot_menu, name='annot_menu'),
    path('login/', views.login_view, name='login_view'),
    path('inscription/', views.inscription, name = 'inscription'),
    path('formulaire/', views.formulaire_genome, name = 'formulaire'),
    re_path('./formulaire/', views.formulaire_genome, name = 're_formulaire'),
    path('formulaire/view_sequence/', views.view_sequence, name="view_sequence"),
    path('annotateur_page/', views.annotateur_page, name='annotateur_page'),
    path('validateur_page/', views.validateur_page, name='validateur_page'),
    path('lecteur_page/', views.lecteur_page, name='lecteur_page'),
    path('logout/', views.logout_view, name='logout'),
    path('sequence/', views.show_sequences, name='sequence'),
    path('validation/', views.validate_annotation, name='validation'),
    re_path('./view_genesequence/', views.view_genesequence, name='view_genesequence'),
    path('assign_annotation/', views.assign_annotation, name = 'assign_annotation'),
    path('blast/', views.blast_view, name='blast'),
    path('annotations_attrib/', views.annotations, name = 'annotations_attrib'),
    path('formulaire_annotation/<int:annotation_id>/', views.formulaire_annotation, name = 'formulaire_annotation'),
    path('success/', views.formulaire_annotation, name = 'success'),
    path('extract_data/', views.extract_data, name = 'extract_data'),
    path('forum/', views.send_message, name = 'forum'),
]

