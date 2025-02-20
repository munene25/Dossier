from django.shortcuts import render
from . import utils
from .forms import ResumeForm

def index(request): # create a function called index that takes a request object
    if request.method == 'POST':
        resume_form = ResumeForm(request.POST)
        if resume_form.is_valid():
            pass
        else:
            pass
    else:
        response = {'resume_form' : ResumeForm()}

    return render(request, 'resumes/resumes.html', response)
