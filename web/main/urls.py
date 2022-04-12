from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('logout/', views.auth_logout, name='logout'),
    path('projects/', views.projects_list, name='projects'),
    path('review/<str:git_user>/<str:git_repo>',
         views.project_review, name='review'
         )
]
