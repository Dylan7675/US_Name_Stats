from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='analysis-home'),
    path('about/', views.about, name='project-about'),

]