from django.urls import path
from . import views


app_name = 'resumes'
urlpatterns = [
    path('', views.upload, name='upload'),
    path('modify/<int:pk>/<str:category>', views.modify, name='modify'),
]