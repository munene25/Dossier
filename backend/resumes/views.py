from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, ListView, DeleteView
from django.template.loader import render_to_string
from django.forms.models import model_to_dict
from django.contrib import messages
from django.http import HttpResponse
from weasyprint import HTML
from .models import ResumeDataModel
from . import utils
from .forms import CreateResumeForm
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
                messages.error(request, f"Server Busy")
                messages.error(request, f"Error: {str(e)}")
            if raw_json:
                #Get Logged in user and create entry on the resume model and link them
                user = request.user
                resume_object = utils.create_resume_object(user, form.cleaned_data["title"], raw_json)
                messages.success(request, "File successfully saved.")
                
                
                return redirect("resumes:personal_information", resume_object.id)
            else:
                messages.error(
                    request,
                    "Error: {'Could Not Upload document at this time, check your file format or try again later'}",
                )

        else:
            messages.error(request, f"Invalid file format or missing field data")

        return render(request, template_name="upload.html", context={"form": utils.FormList.upload})

class CreateView(View):
    def get(self, request):
        return render(request, "create.html")
    
    def post(self, request):
        user=request.user
        form = CreateResumeForm(request.POST)
        if form.is_valid():
            new_resume = utils.create_resume_object(user=user, title=form.cleaned_data["title"], raw_json={})
        
            messages.success(request, "File successfully saved.")
            return redirect("resumes:personal_information", new_resume.id)
        else:
            return redirect("resumes:create",  new_resume.id)
    

class BasicFormView(View):
    """Generate forms for Personal Information and Overview"""

    template_name = "modify.html"
    category = ""

    def dispatch(self, request, *args, **kwargs):
        self.category_form_class = getattr(utils.FormList, self.category)
        self.user_field_form_class = getattr(utils.FormList, "user_defined_field")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        pk = kwargs.get("resume_id", None)
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
            "pk": pk,
        }
        context.update(getattr(utils.Navigation(), self.category))
        return render(request, template_name=self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        pk = kwargs.get("resume_id", None)
        category_form = self.category_form_class(request.POST)
        user_field_form = self.user_field_form_class(request.POST)

        category_data = utils.clean_form(category_form)
        user_data = utils.clean_form(user_field_form)
        utils.update_resume(self.category, pk, category_data, user_data)
        messages.success(request, "Successfully Updated")
        return redirect(f"resumes:{getattr(utils.Navigation(), self.category)['next']}", pk)


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
        pk = kwargs.get("resume_id", None)
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
            "pk": pk,
        }
        context.update(getattr(utils.Navigation(), self.category))
        return render(request, template_name=self.template_name, context=context)

    def post(self, request, **kwargs):
        pk = kwargs.get("resume_id", None)
        category_formset = self.CategoryFormSet(request.POST)
        user_field_form = self.user_field_form_class(request.POST)

        category_data = utils.clean_formset(category_formset)
        user_data = utils.clean_form(user_field_form)


        utils.update_resume(self.category, pk, category_data, user_data)
        messages.success(request, "Successfully Updated")
        if self.category == 'languages':
            return redirect(f"resumes:{getattr(utils.Navigation(), self.category)['finish']}", pk)

        return redirect(f"resumes:{getattr(utils.Navigation(), self.category)['next']}", pk)


class ResumeListView(ListView):
    model = ResumeDataModel
    template_name = "resume_list.html"
    context_object_name = "resumes"

    
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(user=self.request.user).order_by("-created_at")
    

class ResumePreviewView(View):
    def get(self, request, **kwargs):
        resume_id = kwargs.get("resume_id")
        resume = get_object_or_404(ResumeDataModel, pk=resume_id)
        resume_dict = model_to_dict(resume)
        return render(request, 'preview.html', {"data": resume_dict, "resume_id": resume_id})

class DownloadView(View):
    def get(self, request, **kwargs):
        resume_id = kwargs.get("resume_id")
        resume = get_object_or_404(ResumeDataModel, pk=resume_id)
        resume_dict = model_to_dict(resume)
        # Render HTML template with data
        html_string = render_to_string('r_template1.html', {
            "data": resume_dict,
            "pdf_generation": True
        })
        try:
            
            # Generate PDF
            pdf_file = HTML(string=html_string).write_pdf()
            
            # Create safe filename
            auth_name = f"{resume.title}"
            safe_filename = f"Resume_{auth_name}.pdf".replace(" ", "_")
            messages.success(request, "Good luck with your shinny new resume!")
        except Exception as e:
            messages.error(request, f"Could not print resume, check file for errors! {e}")
            return render(request, 'preview.html', {"data": resume_dict, "resume_id": resume_id})
        
        # Prepare response
        response = HttpResponse(pdf_file, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{safe_filename}"'
        response['Content-Length'] = len(pdf_file)
        
        return response

        
class ResumeDeleteView(View):
    def post(self, request, **kwargs):
        pk = kwargs.get("resume_id")
        try:
            resume = ResumeDataModel.objects.get(pk=pk)
            resume.delete()
            messages.success(request, "Resume deleted successfully.")
        except ResumeDataModel.DoesNotExist:
            messages.error(request, "Resume not found.")
        except Exception as e:
            messages.error(request, f"Failed to delete resume: {str(e)}")
        return redirect("resumes:my_resumes")
