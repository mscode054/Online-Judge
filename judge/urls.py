from django.urls import path
from django.views.generic.base import TemplateView
from . import views

app_name='judge'
urlpatterns = [
    path('', TemplateView.as_view(template_name='judge/login.html'), name='login'),
    path('register/', TemplateView.as_view(template_name='judge/register.html'), name='register'),
    path('problems/', views.problems, name='problems'),
    path('<int:pk>/', views.DetailView.as_view(), name='desc'),
    path('<int:problem_id>/verdict/', views.verdict, name='verdict'),
]