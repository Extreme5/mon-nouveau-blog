from django import views
from django.urls import path,include
from .views import *

urlpatterns = [
    path('',home, name="home"),
    path('reservation1',reservation1, name="reservation1"),
    path('reservation2_thalasso',reservation2_thalasso, name="reservation2_thalasso"),
    path('reservation2_sur_mesure',reservation2_sur_mesure, name="reservation2_sur_mesure"),
    path('reservation2_pret',reservation2_pret, name="reservation2_pret"),
    path('reservation_temps',reservation_temps, name="reservation_temps"),
    path('reservation_date',reservation_date, name="reservation_date"),
    path('reservation4',reservation4, name="reservation4"),
    path('nous',nous, name="nous"),
    path('contact',contact, name="contact"),
    path('confirmation',confirmation, name="confirmation"),
    path('thalasso_mesure',thalasso_mesure, name="thalasso_mesure"),
]