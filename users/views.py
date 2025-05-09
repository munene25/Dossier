from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from allauth.account.views import (
    LoginView, 
    SignupView, 
    LogoutView, 
    PasswordResetView, 
    PasswordResetDoneView, 
    PasswordChangeView,
    EmailView,
    PasswordResetFromKeyView,
    ConfirmEmailView,
)
from allauth.account.adapter import DefaultAccountAdapter
from .forms import CustomLoginForm

class DashboardView(generic.TemplateView):
    template_name = 'welcome.html'

class CustomLoginView(LoginView):
    template_name = 'account/login.html'
    form_class = CustomLoginForm

    def form_valid(self, form):
        remember = form.cleaned_data.get('remember')
        if not remember:
            self.request.session.set_expiry(0)
        else:
            self.request.session.set_expiry(1209600)
        return super().form_valid(form)


class CustomLogoutView(LogoutView):
    template_name = 'account/logout.html'

class CustomSignupView(SignupView):
    template_name = 'account/signup.html'
    

class CustomAccountView(EmailView):
    template_name = 'account/account.html'
    pass

class CustomPasswordResetView(PasswordResetView):
    template_name = 'account/password_reset.html'

class CustomPasswordResetFromKeyView(PasswordResetFromKeyView):
    template_name = 'account/password_reset_from_key.html'

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'account/password_reset_done.html'

class CustomConfirmEmailView(ConfirmEmailView):
    template_name = 'account/confirm_email.html'

class CustomPasswordChangeView(PasswordChangeView):
    def get(self, request, *args, **kwargs):
        return self.http_method_not_allowed(request, *args, **kwargs)
    
    def get_success_url(self):
        return '/account/'
