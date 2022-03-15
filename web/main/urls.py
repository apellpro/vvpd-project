from django.urls import path
from . import views


urlpatterns = [
    path('', views.homepage, name='home'),
    path('projects/', views.projects, name='projects'),
    path('info/', views.get_some_information)
]