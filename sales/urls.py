from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),                              #Home page
    path('signup/', views.signup, name='signup'),                   #Registrazione
    path('search/', views.search),                                  #Pagina iniziale ricerca
    path('search/users/', views.search_users),                      #Ricerca utente
    path('search/users/results', views.SearchUsersResults.as_view(), name='search_student_results'),             #Risultati ricerca utente
    path('users/<str:username>/suggested', views.first_page),       #Consigli intelligenti
    #path('users/<str:username>/personal', views.personal),          #Pagina personale utente
    path('users/<str:username>/profile', views.profile),            #Profilo utente
    #path('search/ads/', views.search_ad),                           #Ricerca annuncio
    path('ads/<str:ad_pk>', views.ad_details),                      #Annuncio
    #path('search/titles/', views.search_title),                     #Titolo
    #path('titles/<str:title_pk>', views.title_details),             #Titolo

]