from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('logout/', views.auth_logout, name='logout'),
    path('projects/', views.projects_list, name='projects'),
    path('review/<str:git_user>/<str:git_repo>',
         views.project_review, name='review'
         ),
    path('api/getcommits', views.ajax_commits, name='ajaxCommits'),
    path('api/getuserdelta', views.ajax_delta, name='ajaxDelta'),
    path('functions/addyeargroup/', views.year_group, name='add_year_group'),
    path('functions/addproject/', views.project, name='add_project'),
    path('functions/addpersonaltag/', views.tag,
         name='add_personal_tag')
]
