
from django.contrib import admin
from django.urls import path, include
from genome import urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('genome.urls')),
    path('login/',include('genome.urls')),
    path('inscription/', include('genome.urls')),
    path('formulaire/', include('genome.urls')),
    path('annotations/', include('genome.urls'))

]

"""
    path('/menu/', views.annot_menu, name='annot_menu'),
    path('annotations/', views.annotation_list, name='annotation_list'),
    path('', views.annot_menu, name='annot_menu'),
    path('login/', views.login_view, name='login_view'),
    path('inscription/', views.inscription, name = 'inscription'),
    path('formulaire/', views.formulaire_genome, name = 'formulaire'),
]
"""
