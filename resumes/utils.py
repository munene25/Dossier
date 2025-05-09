import pdfplumber
from google import genai
from pathlib import Path
from pydantic import BaseModel
from typing import Optional, List, Dict
from django.conf import settings
from .models import ResumeDataModel
from . import forms

from django.forms import formset_factory



class Item(BaseModel):
    item: Optional[str] = None


class Extras(BaseModel):
    category_name: Optional[str] = None
    description: Optional[str] = None


class Skills(BaseModel):
    category_name: Optional[str]
    description: Optional[list[str]] = None


class Referees(BaseModel):
    name: Optional[str] = None
    occupation: Optional[str] = None
    institution: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None


class Education(BaseModel):
    institution: Optional[str] = None
    degree: Optional[str] = None
    location: Optional[str] = None
    graduation_date: Optional[str] = None
    description: Optional[List[str]] = None


class ProfessionalExperience(BaseModel):
    job_title: Optional[str] = None
    company: Optional[str] = None
    department: Optional[str] = None
    location: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    responsibilities: Optional[List[str]] = None


class Overview(BaseModel):
    text: str = None


class PersonalInformation(BaseModel):
    first_name: Optional[str] = None 
    last_name: Optional[str] = None 
    career: Optional[str] = None 
    phone: Optional[str] = None
    email: Optional[str] = None
    linkedin: Optional[str] = None
    external_link: Optional[str] = None


class UserDefinedFields(BaseModel):
    personal_information: Optional[str] = None
    overview: Optional[str] = None
    education: Optional[str] = None
    professional_experience: Optional[str] = None
    skills: Optional[str] = None
    referees: Optional[str] = None
    certificates: Optional[str] = None
    languages: Optional[str] = None
    

class Resume(BaseModel):
    user_defined_fields: UserDefinedFields
    personal_information: PersonalInformation
    overview: Overview
    education: List[Education]
    professional_experience: List[ProfessionalExperience]
    skills: List[Skills]
    referees: List[Referees]
    extras: List[Extras]
    certificates: List[Item]
    languages: List[Item]

class Navigation:
    personal_information = {"back": None, "next": "overview"}
    overview = {"back": "personal_information", "next": "education"}
    education = {"back": "overview", "next": "professional_experience"}
    professional_experience = {"back": "education", "next": "skills"}
    skills = {"back": "professional_experience", "next": "referees"}
    referees = {"back": "skills", "next": "extras"}
    extras = {"back": "referees", "next": "certificates"}
    certificates = {"back": "extras", "next": "languages"}
    languages = {"back": "certificates", "finish": "render_resume"}

class FormList:
    user_defined_field = forms.UserDefinedFieldForm
    education = forms.EducationForm
    professional_experience = forms.ProfessionalExperienceForm
    skills = forms.DescriptionForm
    referees = forms.RefereesForm
    extras = forms.DescriptionForm
    certificates = forms.ItemForm
    languages = forms.ItemForm
    personal_information = forms.PersonalInformationForm
    overview = forms.OverviewForm
    upload = forms.ResumeUploadForm
    nav_form = forms.NavForm

sys_prmpt = """ 
You are a resume parsing software. Extract and structure the data into JSON format, categorizing it under relevant sections.
### **Rules:**  
- **Extract only meaningful content**: Ignore section dividers, bullet points, repeated headers, and unnecessary formatting while preserving logical structure.  
- **Map sections intelligently**: If a resume uses "Work History" instead of "ProfessionalExperience," map it accordingly in the UserDefinedFields. If a section is unclear, place it under "Extras."  
- **Rewrite "Extras" descriptions**: Summarize the "description" field into a natural, concise first-person paragraph(s) for each entry in the category that is clear and easy to read.  
- **List all certificates**: Include every mentioned certificate under "Certificates."  
- **Extract each language separately**: Ensure individual entries (e.g., "English," "French").  
- **Maintain consistency**: Include all predefined sections, even if empty.  
- **Standardize dates**: Format all dates as "Month, YYYY." If no end date is provided, use "Present."

"""


def parse_resume(file_object):
    raw_extracted_text = ""

    with pdfplumber.open(file_object) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                raw_extracted_text += text + "\n"

    return generate(raw_extracted_text)


def generate(raw_extracted_text):
    GOOGLE_API_KEY = settings.GOOGLE_API_KEY
    client = genai.Client(api_key=GOOGLE_API_KEY)

    response = client.models.generate_content(
        model = "gemini-2.0-flash",
        contents=f"Resume is as Follows: \n {raw_extracted_text} \n Parse this resume for me",
        config={
            "response_mime_type": "application/json",
            "system_instruction": sys_prmpt,
            "response_schema": Resume,
        },
    )
    return response.text

def create_resume_object(user, title, raw_json):
    resume = ResumeDataModel.objects.create(
        user = user,
        title = title,
        user_defined_fields=raw_json.get("user_defined_fields", {}),
        personal_information=raw_json.get("personal_information", {}),
        overview=raw_json.get("overview", {}),
        education=raw_json.get("education", []),
        professional_experience=raw_json.get("professional_experience", []),
        skills=raw_json.get("skills", {}),
        referees=raw_json.get("referees", []),
        extras=raw_json.get("extras", []),
        certificates=raw_json.get("certificates", []),
        languages=raw_json.get("languages", []),
    )
    if resume.user_defined_fields:
        for key, value in resume.user_defined_fields.items():
            if value is None:
                resume.user_defined_fields[key] = key.replace("_", " ").title()
        resume.save()
    else:
        resume.user_defined_fields = {"personal_information": "Personal Information", "overview": "Overview", "education": "Education", "professional_experience": "Professional Experience", "skills": "Skills", "referees": "Referees", "certificates": "Certificates", "languages": "Languages"}
        resume.save()
    return resume

def get_resume_data(resume_object, category):
    category_data = getattr(resume_object, category)
    if category != "extras":
        field_name = resume_object.user_defined_fields[category]
    else:
        field_name = 'Extras'
    return {"field_name": field_name, "category_data": category_data}

def update_resume(category: str, pk: int, data: any, user_defined_data: dict):
    resume = ResumeDataModel.objects.get(pk=pk)
    updated = False  # Track if any changes were made

    # Update JSON field safely
    if category in resume.user_defined_fields:
        resume.user_defined_fields[category] = user_defined_data.get('user_defined_field', None)
        updated = True

    # Update model attribute if it exists
    if hasattr(resume, category):
        setattr(resume, category, data)
        updated = True

    # Save only if something was modified
    if updated:
        resume.save()

    return updated

def clean_form(form):
    return form.cleaned_data if form.is_valid() else form.errors

        
def clean_formset(formset):
    if formset.is_valid():
        return [
            form for form in formset.cleaned_data if any(form.values())
        ]
    else:
        return formset.errors
        
    

if (__name__) == "__main__":
    pass