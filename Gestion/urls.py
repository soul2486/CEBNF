from django.contrib import admin
from django.urls import path, include
from .views import Home, Classes, Eleves_salle, Historique, premiere_tranche, HistoriqueDay

urlpatterns = [
    path('', Home, name="accueil" ),
    path('classes/', Classes, name="classes"),
    path('historique_day/', HistoriqueDay, name="historique_day"),
    path('classes/<int:pk>/', Eleves_salle, name="Eleves_salle"),
    path('historique/<int:pk>/', Historique, name="historique"),
    path('premiere_tranche/', premiere_tranche, name="premiere_tranche"),

]