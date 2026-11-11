"""URLs de la aplicación prendas."""

from django.urls import path

from . import views

app_name = 'prendas'

urlpatterns = [
    path('', views.home, name='home'),
    path('catalogo/', views.PrendaListView.as_view(), name='catalogo'),
    path('prenda/<int:pk>/', views.PrendaDetailView.as_view(), name='detalle'),
]
