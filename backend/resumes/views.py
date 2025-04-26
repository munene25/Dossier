from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, ListView, DeleteView
from django.template.loader import render_to_string
from django.forms.models import model_to_dict
from django.contrib import messages
from django.urls import reverse_lazy
from .models import ResumeDataModel
from . import utils
import json


class UploadView(View):
    def get(self, request):
        return render(
            request,
            template_name="upload.html",
            context={"form": utils.FormList.upload},
        )

    def post(self, request):
        form = utils.FormList.upload(request.POST, request.FILES)

        if form.is_valid():
            raw_json = None
            try:
                file_data = form.cleaned_data["pdf_file"]
                raw_json = json.loads(utils.parse_resume(file_data))
            except Exception as e:
                messages.error(request, f"Error: {e}")
            if raw_json:
                #Get Logged in user and create entry on the resume model and link them
                user = request.user
                resume_object = utils.create_resume_object(user, raw_json)
                messages.success(request, "File successfully saved.")
                
                request.session["resume_id"] = resume_object.id
                return redirect("resumes:personal_information")
            else:
                messages.error(
                    request,
                    "Error: {'Could Not parse document at this time, check your file type or try again later'}",
                )

        else:
            messages.error(request, f"Invalid file format")

        return render(request, template_name="upload.html", context={"form": utils.FormList.upload})

class BasicFormView(View):
    """Generate forms for Personal Information and Overview"""

    template_name = "modify.html"
    category = ""

    def dispatch(self, request, *args, **kwargs):
        self.category_form_class = getattr(utils.FormList, self.category)
        self.user_field_form_class = getattr(utils.FormList, "user_defined_field")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        pk = request.session.get("resume_id")
        resume_object = get_object_or_404(ResumeDataModel, pk=pk)
        resume_data = utils.get_resume_data(resume_object, self.category)
        user_field_form = self.user_field_form_class(
            initial={"user_defined_field": resume_data["field_name"]}
        )
        category_form = self.category_form_class(resume_data["category_data"])
        context = {
            "user_field_form": user_field_form,
            "form": category_form,
            "category": self.category,
        }
        context.update(getattr(utils.Navigation(), self.category))
        return render(request, template_name=self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        pk = request.session.get("resume_id")
        category_form = self.category_form_class(request.POST)
        user_field_form = self.user_field_form_class(request.POST)

        category_data = utils.clean_form(category_form)
        user_data = utils.clean_form(user_field_form)
        utils.update_resume(self.category, pk, category_data, user_data)
        return redirect(f"resumes:{getattr(utils.Navigation(), self.category)['next']}")


class FormsetView(View):
    """Generate forms for Personal Information and Overview"""

    template_name = "modify.html"
    category = ""

    def dispatch(self, request, *args, **kwargs):
        self.category_form_class = getattr(utils.FormList, self.category)
        self.CategoryFormSet = utils.formset_factory(self.category_form_class, extra=1)
        self.user_field_form_class = getattr(utils.FormList, "user_defined_field")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, **kwargs):
        pk = request.session.get("resume_id")
        resume_object = get_object_or_404(ResumeDataModel, pk=pk)
        resume_data = utils.get_resume_data(resume_object ,self.category)

        category_form = self.CategoryFormSet(initial=resume_data["category_data"])
        user_field_form = self.user_field_form_class(
            initial={"user_defined_field": resume_data["field_name"]}
        )
        context = {
            "user_field_form": user_field_form,
            "formset": category_form,
            "category": self.category,
        }
        context.update(getattr(utils.Navigation(), self.category))
        return render(request, template_name=self.template_name, context=context)

    def post(self, request, **kwargs):
        pk = request.session.get("resume_id")
        category_formset = self.CategoryFormSet(request.POST)
        user_field_form = self.user_field_form_class(request.POST)

        category_data = utils.clean_formset(category_formset)
        user_data = utils.clean_form(user_field_form)

        utils.update_resume(self.category, pk, category_data, user_data)
        messages.success(request, "Successfully Updated")
        if self.category == 'languages':
            return redirect(f"resumes:{getattr(utils.Navigation(), self.category)['finish']}")

        return redirect(f"resumes:{getattr(utils.Navigation(), self.category)['next']}")


def render_resume(request, *args ,**kwargs):
    resume = get_object_or_404(ResumeDataModel, pk=request.session.get("resume_id"))
    resume_dict = model_to_dict(resume)
    html_string = render_to_string('render_resume.html', {"data": resume_dict})
    with open("input.html", "w")as file:
        file.write(html_string)
    utils.print_pdf()
    return render(request, 'render_resume.html', {"data": resume_dict})

def create(request):
    pass

class ResumeListView(ListView):
    model = ResumeDataModel
    template_name = "resume_list.html"
    context_object_name = "resumes"

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(user=self.request.user).order_by("-created_at")
    

def select_resume(request):
    if request.method == "POST":
        Form = getattr(utils.FormList, "nav_form")
        form = Form(request.POST)
        print(form)
        if form.is_valid():
            
            request.session["resume_id"] = form.cleaned_data["resume_id"]
            return redirect(f"resumes:{form.cleaned_data["next_url"]}")
        else:
            return redirect("users:dashboard")
        
class ResumeDeleteView(DeleteView):
    model = ResumeDataModel
    success_url = reverse_lazy('resume:my_resumes')
