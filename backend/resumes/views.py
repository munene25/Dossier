from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.http import HttpResponse
from .forms import ResumeForm



def index(request):
    if request.method == 'POST':
        form = ResumeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'File successfully saved')
            return redirect(reverse('resumes:index'))
        else:
            return HttpResponse(form.errors)
        
    else:
        form = {'form': ResumeForm()}
    return render(request, 'resumes/upload.html', form)