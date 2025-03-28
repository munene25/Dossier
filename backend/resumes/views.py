from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib import messages
from django.views.generic import View
from .models import DataModel, ResumeModel
from . import forms
from .utils import parse_resume
from rest_framework.response import Response
from rest_framework.decorators import api_view
import json


class UploadView(View):
    def get(self, request):
        context = {"form": forms.ResumeForm()}
        return render(request, template_name="resumes/upload.html", context=context)

    def post(self, request):
        form = forms.ResumeForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                new_resume = form.save()
                raw_json = json.loads(parse_resume(new_resume.file.path))

                DataModel.objects.create(
                    resume_model=new_resume,
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
                messages.success(request, "File successfully saved.")
                return redirect("resumes:personal_information", pk=new_resume.id)
            except Exception as e:
                messages.error(request, f"Error: {e}")
        else:
            context = {"form": forms.ResumeForm()}
            messages.error(request, f"Invalid file format")
        return render(request, template_name="resumes/upload.html", context=context)


class Navigation:
    personal_information = {"back": None, "next": "overview"}
    overview = {"back": "personal_information", "next": "education"}
    education = {"back": "overview", "next": "professional_experience"}
    professional_experience = {"back": "education", "next": "skills"}
    skills = {"back": "professional_experience", "next": "referees"}
    referees = {"back": "skills", "next": "extras"}
    extras = {"back": "referees", "next": "certificates"}
    certificates = {"back": "extras", "next": "languages"}
    languages = {"back": "certificates", "next": None}


class BasicFormView(View, Navigation):
    """Generate forms for Personal Information and Overview"""

    template_name = "resumes/modify-form.html"
    category_list = {
        "user_field": forms.UserDefinedFieldForm,
        "personal_information": forms.PersonalInformationForm,
        "overview": forms.OverviewForm,
    }
    category = ""

    def dispatch(self, request, *args, **kwargs):
        self.category_form_class = self.category_list[self.category]
        self.user_field_form_class = self.category_list["user_field"]
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):

        resume_object = ResumeModel.objects.get(pk=kwargs.get("pk"))
        if resume_object and hasattr(resume_object, "data_model"):
            category_data = getattr(resume_object.data_model, self.category)

            user_defined_fields = getattr(
                resume_object.data_model, "user_defined_fields"
            )

            self.field_name = user_defined_fields.get(self.category)
            if self.field_name == None:
                self.field_name = self.category.title().replace("_", " ")

            user_field_form = self.user_field_form_class(
                initial={"user_defined_field": self.field_name}
            )
            category_form = self.category_form_class(category_data)

        else:
            category_form = self.category_form_class()
            user_field_form = self.user_field_form_class(
                initial={"user_defined_field": self.field_name}
            )
        context = {
            "user_field_form": user_field_form,
            "form": category_form,
            "category": self.category,
            "pk": kwargs.get("pk"),
        }
        context.update(getattr(Navigation(), self.category))
        return render(request, template_name=self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        category_form = self.category_form_class(request.POST)
        user_field_form = self.user_field_form_class(request.POST)

        return HttpResponse(f"{category_form} and  {user_field_form}")


class FormsetView(View, Navigation):
    """Generate forms for Personal Information and Overview"""

    template_name = "resumes/modify-form.html"
    category_list = {
        "user_field": forms.UserDefinedFieldForm,
        "education": forms.EducationForm,
        "professional_experience": forms.ProfessionalExperienceForm,
        "skills": forms.DescriptionForm,
        "referees": forms.RefereesForm,
        "extras": forms.DescriptionForm,
        "certificates": forms.ItemForm,
        "languages": forms.ItemForm,
    }
    category = ""

    def dispatch(self, request, *args, **kwargs):
        self.category_form_class = self.category_list[self.category]
        self.CategoryFormSet = forms.formset_factory(self.category_form_class, extra=0)
        self.user_field_form_class = self.category_list["user_field"]
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, **kwargs):
        pk = kwargs.get("pk")
        resume_object = ResumeModel.objects.get(pk=pk)

        if resume_object and hasattr(resume_object, "data_model"):
            category_data = getattr(resume_object.data_model, self.category)

            user_defined_fields = getattr(
                resume_object.data_model, "user_defined_fields"
            )
            self.user_field = user_defined_fields.get(self.category)
            if self.user_field == None:
                self.user_field = self.category.title().replace("_", " ")
            category_form = self.CategoryFormSet(initial=category_data)
            user_field_form = self.user_field_form_class(
                initial={"user_defined_field": self.user_field}
            )

        else:
            category_form = self.CategoryFormSet()
            user_field_form = self.user_field_form_class(
                initial={"user_defined_field": self.user_field}
            )
        context = {
            "user_field_form": user_field_form,
            "formset": category_form,
            "category": self.category,
            "pk": pk,
        }
        context.update(getattr(Navigation(), self.category))
        return render(request, template_name=self.template_name, context=context)

    def post(self, request, **kwargs):
        pk = kwargs.get("pk")
        category_formset = self.CategoryFormSet(request.POST)
        user_field_form = self.user_field_form_class(request.POST)

        # Collect submitted data without saving
        category_data = (
            [form.cleaned_data for form in category_formset]
            if category_formset.is_valid()
            else category_formset.errors
        )
        user_data = (
            user_field_form.cleaned_data
            if user_field_form.is_valid()
            else user_field_form.errors
        )

        return HttpResponse(
            f"<h2>Submitted Data</h2> <pre>{category_data}</pre> <pre>{user_data}</pre>"
        )
