from django.urls import path
from django.views.generic.base import TemplateView
from . import views

app_name='judge'
urlpatterns = [
    path('', views.login_req, name='login'),
    path('logout/', views.logout_request, name='logout'),
    path('register/', views.register, name='register'),
    path('problems/', views.problems, name='problems'),
    path('problems/<int:pk>/', views.DetailView.as_view(), name='desc'),
    path('problems/<int:problem_id>/verdict/', views.submission, name='submission'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
]