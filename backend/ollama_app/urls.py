from django.urls import path
from . import views

app_name = 'ollama'
urlpatterns = [
    path('', views.generate, name = 'generate')
]