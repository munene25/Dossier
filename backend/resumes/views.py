from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from .models import ResumeDataModel, ResumeModel
from .forms import ResumeForm
from .utils import parse_resume
from rest_framework.response import Response
from rest_framework.decorators import api_view
import json

def index(request):
    context = {'form': ResumeForm()}
    if request.method == 'POST':
        form = ResumeForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                new_resume = form.save()
                raw_json = json.loads(parse_resume(new_resume.file.path))
                
                new_resume.raw_json = raw_json
                new_resume.save()
                ResumeDataModel.objects.create(
                    resume=new_resume,
                    user_defined_fields=raw_json.get("UserDefinedFields", {}),
                    personal_information=raw_json.get("PersonalInformation", {}),
                    overview=raw_json.get("Overview", {}),
                    professional_experience=raw_json.get("ProfessionalExperience", []),
                    education=raw_json.get("Education", []),
                    skills=raw_json.get("Skills", {}),
                    referees=raw_json.get("Referees", []),
                    extras=raw_json.get("Extras", []),
                    certificates=raw_json.get("Certificates", []),
                    languages=raw_json.get("Languages", [])
                )
                messages.success(request, 'File successfully saved.')
                return redirect(reverse('resumes:modify_personal_information', kwargs={'pk':new_resume.id}))
            
            except Exception as e:
                messages.error(request, f'Error: {e}')    
        return render(request, template_name='resumes/upload.html', context=context)
    # Render form for both GET and invalid POST cases
    return render(request, template_name='resumes/upload.html', context=context)


def modify_personal_information(request, pk:int):
    if request.method == 'POST':
        post_data = request.POST
        print(post_data)
        messages.success(request, 'Successful')
        return redirect(reverse('resumes:index'))
    resume_object = ResumeModel.objects.get(pk=pk)
    context = {
        'resume_id': pk,
        'user_defined_fields' : resume_object.data.user_defined_fields,
        'personal_information' : resume_object.data.personal_information
    }
    return render(request, template_name='resumes/personal_information.html', context=context)