from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponse
from .models import DataModel, ResumeModel
from . import forms
from .utils import parse_resume
from rest_framework.response import Response
from rest_framework.decorators import api_view
import json

def upload(request):
    if request.method == 'POST':
        form = forms.ResumeForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                new_resume = form.save()
                raw_json = json.loads(parse_resume(new_resume.file.path))
                
                new_resume.raw_json = raw_json
                new_resume.save()
                DataModel.objects.create(
                    resume_model=new_resume,
                    user_defined_fields=raw_json.get("user_defined_fields", {}),
                    personal_information=raw_json.get("personal_information", {}),
                    overview=raw_json.get("overview", {}),
                    professional_experience=raw_json.get("professional_experience", []),
                    education=raw_json.get("education", []),
                    skills=raw_json.get("skills", {}),
                    referees=raw_json.get("referees", []),
                    extras=raw_json.get("extras", []),
                    certificates=raw_json.get("certificates", []),
                    languages=raw_json.get("languages", [])
                )
                messages.success(request, 'File successfully saved.')
                return redirect('resumes:modify', pk=new_resume.id)
            
            except Exception as e:
                messages.error(request, f'Error: {e}')
        messages.error(request, f'Invalid file format')
    context = {'form': forms.ResumeForm()}
    return render(request, template_name='resumes/upload.html', context=context)


def modify(request, pk:int, category:str):
    category_list = {
            'personal_information': forms.PersonalInformationForm,
            'overview': forms.OverviewForm,
            # 'professional_experience': forms.ProfessionalExperienceForm,
            # 'skills': forms.SkillsForm,
            # 'education': forms.RefereesForm,
            # 'extras': forms.RefereesForm,
            # 'certifications': forms.RefereesForm,
            # 'languages': forms.RefereesForm
        }
    form_class = category_list[category]
    
    context={
        'pk': pk,
        'category': list(category_list.keys()),
    }

    default_values = {
        'UserDefinedField': category.replace('_', ' ').title()
    }
    if request.method == 'POST':
        form = form_class(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            user_defined_field = {key: value for key, value in form.cleaned_data.items() if key == 'UserDefinedField'} 
            category_data = {key: value for key, value in form.cleaned_data.items() if key != 'UserDefinedField'} 
            return HttpResponse(f'<p>{category_data}<p> <p>{user_defined_field}<p>', status=200)
        else:
            return HttpResponse('Nope')
        
    if request.method == "GET":
        resume_object = ResumeModel.objects.get(pk=pk)
        default_values.update(getattr(resume_object.data_model, category))
        
        form = form_class(initial=default_values)
        context.update({'form': form})
        return render(request, 'resumes/modify.html', context=context)
        