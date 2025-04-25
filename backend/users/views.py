from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from resumes.models import ResumeDataModel

class SignUpView(generic.CreateView):
    form_class    = UserCreationForm
    template_name = 'signup.html'
    success_url   = reverse_lazy('users:login')

    def form_valid(self, form):
        # First save the new user
        response = super().form_valid(form)
        # Then add your message
        messages.success(self.request, "Account created succesfully — please log in.")
        return response


class DashboardView(LoginRequiredMixin, generic.TemplateView):
    def get(self, request, *args, **kwargs):
        resume_object = ResumeDataModel.objects.filter(user=request.user).latest("id")
        request.session["resume_id"] = resume_object.id
        return super().get(request, *args, **kwargs)
    template_name = 'welcome.html'
