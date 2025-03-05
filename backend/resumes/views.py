from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from .forms import ResumeForm
from .utils import parse_resume

def index(request):
    if request.method == 'POST':
        form = ResumeForm(request.POST, request.FILES)
        if form.is_valid():
            resume = form.save()
            messages.success(request, 'File successfully saved.')
            request.session['raw_pdf_text'] = parse_resume(resume.pdf_file.path)
            return redirect(reverse('ollama:generate'))
        messages.error(request, 'There was an error with your submission. Please submit a valid pdf file')
    
    # Render form for both GET and invalid POST cases
    context = {'form': ResumeForm()}
    return render(request, 'resumes/upload.html', context)

