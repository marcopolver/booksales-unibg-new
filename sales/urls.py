from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),                      #Home page
    path('signup/', views.signup, name='signup'),           #Registrazione
    path('<str:username>/suggested', views.first_page),     #Consigli intelligenti
    path('<str:username>', views.profile),                  #Profilo utente
    path('ads/<str:ad_pk>', views.ad_details),              #Annuncio
    #path('titles/<str:title_pk>', views.title_details),    #Titolo
]