from django.urls import path, re_path
from . import views
from django.views.generic import RedirectView

from django.shortcuts import render

urlpatterns = [
    path("", RedirectView.as_view(pattern_name="dashboard", permanent=True), name="root-redirect"),

    # Auth views
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('login/', views.CustomLoginView.as_view(), name='account_login'),
    path('signup/', views.CustomSignupView.as_view(), name='account_signup'),
    path('logout/', views.CustomLogoutView.as_view(), name='account_logout'),

    # Account management
    path('account/', views.CustomAccountView.as_view(), name='account_email'),  # if overriding email management
    path('password/change/', views.CustomPasswordChangeView.as_view(), name='account_change_password'),
    
    path('password/reset/', views.CustomPasswordResetView.as_view(), name='account_reset_password'),
    re_path(r"^password/reset/key/(?P<uidb36>[0-9A-Za-z]+)-(?P<key>.+)/$", views.CustomPasswordResetFromKeyView.as_view(), name='account_reset_password_from_key'),
    re_path(r"^confirm-email/(?P<key>[-:\w]+)/$",views.CustomConfirmEmailView.as_view(), name="account_confirm_email",),
    path('password/reset/done/', views.CustomPasswordResetDoneView.as_view(), name='account_reset_password_done'),
]


