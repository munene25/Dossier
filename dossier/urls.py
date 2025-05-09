"""
URL configuration for dossier project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.shortcuts import render
from django.conf.urls import handler404
from django.conf.urls.static import static
from users import views


def custom_404(request, exception=None):
    return render(request, '404.html', status=429)
handler404 = custom_404

urlpatterns = [
    path("admin-manage/", admin.site.urls),
    path("resumes/", include("resumes.urls", namespace="resumes")),
    path("", include("users.urls")),
]
