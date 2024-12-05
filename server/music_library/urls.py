from django.urls import path
from . import views

urlpatterns = [
    path('', views.indexSlugless, name='index-slugless'),
    path('upload', views.upload, name="upload"), # upload va prima di <slug:slug> altrimenti upload dimenta uno slug
    path('<slug:slug>', views.index, name='index'),
    path('artist/<slug:artist_slug>', views.artist_page, name='artist-page'),
    path('login/', views.logIn, name='login'),
    path('logout/', views.logOut, name='logout'),
]