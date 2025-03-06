from django.urls import path
from . import views


app_name = 'resumes'
urlpatterns = [
    path('', views.index, name='index'),
    path('modify/<int:pk>/', views.modify_personal_information, name='modify_personal_information'),
]