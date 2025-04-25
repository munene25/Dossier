from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.views.generic import RedirectView

app_name = "users"
urlpatterns = [
    path(
        "",
        RedirectView.as_view(pattern_name="users:dashboard", permanent=True),
        name="root-redirect",
    ),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
]