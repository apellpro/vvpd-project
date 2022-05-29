from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('logout/', views.auth_logout, name='logout'),
    path('projects/', views.projects_list, name='projects'),
    path('personal/', views.personal, name='personal'),
    path('review/<str:git_user>/<str:git_repo>',
         views.project_review, name='review'
         ),
    path('api/getcommits', views.ajax_commits),
    path('api/getuserdelta', views.ajax_delta),
    path('api/mainyeargroup', views.ajax_main_year),
    path('ajax/deletetag', views.ajax_delete_tag),
    path('ajax/boundtag', views.ajax_bound_tag),
    path('ajax/unboundtag', views.ajax_unbound_tag),
    path('functions/addyeargroup/', views.year_group, name='add_year_group'),
    path('functions/addproject/', views.project, name='add_project'),
    path('functions/addpersonaltag/', views.tag,
         name='add_personal_tag'),
    path('changepassword/', views.change_password, name='change_password'),
    path('search/', views.guest_search, name='search')
]
