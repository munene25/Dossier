from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib import messages
from django.views.generic import View
from .models import ResumeDataModel
from . import forms
from . import utils
from rest_framework.response import Response
from rest_framework.decorators import api_view
import json


class UploadView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.context = {"form": forms.ResumeUploadForm}

    def get(self, request):
        return render(request, template_name="upload.html", context=self.context)

    def post(self, request):
        form = forms.ResumeUploadForm(request.POST, request.FILES)

        if form.is_valid():
            try:
                file_data = form.cleaned_data["pdf_file"]
            except Exception as e:
                messages.error(request, f"Error: {e}")

            raw_json = json.loads(utils.parse_resume(file_data))
            if raw_json:
                resume = utils.create_resume_object(raw_json)
                messages.success(request, "File successfully saved.")
                return redirect("resumes:personal_information", pk=resume.pk)
            else:
                messages.error(
                    request,
                    f"Error: {'Could Not parse document at this time, check your file type or try again later'}",
                )

        else:
            messages.error(request, f"Invalid file format")
        return render(request, template_name="upload.html", context=self.context)


class BasicFormView(View):
    """Generate forms for Personal Information and Overview"""

    template_name = "modify-form.html"
    category_list = {
        "user_defined_field": forms.UserDefinedFieldForm,
        "personal_information": forms.PersonalInformationForm,
        "overview": forms.OverviewForm,
    }
    category = ""

    def dispatch(self, request, *args, **kwargs):
        self.category_form_class = self.category_list[self.category]
        self.user_field_form_class = self.category_list["user_defined_field"]
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):

        resume_object = ResumeDataModel.objects.get(pk=kwargs.get("pk"))
        if resume_object:
            category_data = getattr(resume_object, self.category)

            user_defined_fields = getattr(resume_object, "user_defined_fields")

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
        context.update(getattr(utils.Navigation(), self.category))
        return render(request, template_name=self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        category_form = self.category_form_class(request.POST)
        user_field_form = self.user_field_form_class(request.POST)
        
        category_data = clean_form(category_form)
        user_data = clean_form(user_field_form)
        update_resume(self.category, pk, category_data, user_data)
        return redirect(f"resumes:{self.category}", pk=pk)



class FormsetView(View):
    """Generate forms for Personal Information and Overview"""

    template_name = "modify-form.html"
    category_list = {
        "user_defined_field": forms.UserDefinedFieldForm,
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
        self.CategoryFormSet = forms.formset_factory(self.category_form_class, extra=1)
        self.user_field_form_class = self.category_list["user_defined_field"]
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, **kwargs):
        pk = kwargs.get("pk")
        resume_object = ResumeDataModel.objects.get(pk=pk)

        if resume_object:
            category_data = getattr(resume_object, self.category)

            user_defined_fields = getattr(resume_object, "user_defined_fields")
            self.user_defined_field = user_defined_fields.get(self.category)
            if self.user_defined_field == None:
                self.user_defined_field = self.category.title().replace("_", " ")
            category_form = self.CategoryFormSet(initial=category_data)
            user_field_form = self.user_field_form_class(
                initial={"user_defined_field": self.user_defined_field}
            )

        else:
            category_form = self.CategoryFormSet()
            user_field_form = self.user_field_form_class(
                initial={"user_defined_field": self.user_defined_field}
            )
        context = {
            "user_field_form": user_field_form,
            "formset": category_form,
            "category": self.category,
            "pk": pk,
        }
        context.update(getattr(utils.Navigation(), self.category))
        return render(request, template_name=self.template_name, context=context)

    def post(self, request, **kwargs):
        pk = kwargs.get("pk")
        category_formset = self.CategoryFormSet(request.POST)
        user_field_form = self.user_field_form_class(request.POST)

        # Collect submitted data without saving

        category_data = clean_formset(category_formset)
        user_data = clean_form(user_field_form)

        update_resume(self.category, pk, category_data, user_data)
        messages.success(request, "Successfully Updated")
        return redirect(f"resumes:{self.category}", pk=pk)


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
        
