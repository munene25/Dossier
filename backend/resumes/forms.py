from django import forms
from .models import ResumeModel
from django.forms import formset_factory


class ResumeForm(forms.ModelForm):
    class Meta:
        model = ResumeModel
        fields = ["file"]
        labels = {"file": "Upload Your Resume (PDF Only)"}

    def clean_file(self):
        file = self.cleaned_data["file"]  # pdf_file is how we stored it
        if file.content_type != "application/pdf":
            raise forms.ValidationError("Only PDF Files are Allowed")

        # We can check for file size later
        return file


class UserDefinedFieldForm(forms.Form):
    user_defined_field = forms.CharField(
        label="Section",
        widget=forms.TextInput(attrs={"placeholder": "Category"}),
        required=False,
    )


class PersonalInformationForm(forms.Form):
    name = forms.CharField(required=False)
    phone = forms.CharField(required=False)
    email = forms.CharField(required=False)
    linkedin = forms.CharField(required=False)
    external_link = forms.CharField(
        label="External link or Porfolio",
        widget=forms.TextInput(attrs={"placeholder": "portfolio.com"}),
        required=False,
    )


class OverviewForm(forms.Form):
    text = forms.CharField(
        label="",
        required=False,
        widget=forms.Textarea(
            attrs={
                "rows": 10,
                "cols": 60,
                "placeholder": "Brief Summary of yourself, work-experience, education and related data",
            }
        ),
    )


class EducationForm(forms.Form):
    institution = forms.CharField(required=False)
    degree = forms.CharField(required=False)
    location = forms.CharField(required=False)
    graduation_date = forms.CharField(required=False)
    description = forms.CharField(
        label="",
        required=False,
        widget=forms.Textarea(
            attrs={"rows": 10, "cols": 60, "placeholder": "Skills Acquired"}
        ),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Modify self.initial directly, since Django sets it automatically
        list_data = self.initial.get("description", [])

        if isinstance(list_data, list):
            self.initial["description"] = "\n".join(list_data)

    def clean_responsibilities(self):
        submited_list_data = self.cleaned_data.get("description", "")
        return submited_list_data.splitlines()


class ProfessionalExperienceForm(forms.Form):
    company = forms.CharField(required=False)
    job_title = forms.CharField(required=False)
    department = forms.CharField(required=False)
    location = forms.CharField(required=False)
    start_date = forms.CharField(required=False)
    end_date = forms.CharField(required=False)
    responsibilities = forms.CharField(
        label="",
        required=False,
        widget=forms.Textarea(
            attrs={"rows": 10, "cols": 60, "placeholder": "Responsibilities"}
        ),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Modify self.initial directly, since Django sets it automatically
        list_data = self.initial.get("responsibilities", [])

        if isinstance(list_data, list):
            self.initial["responsibilities"] = "\n".join(list_data)

    def clean_responsibilities(self):
        submited_list_data = self.cleaned_data.get("responsibilities", "")
        return submited_list_data.splitlines()


class RefereesForm(forms.Form):
    name = forms.CharField(required=False)
    occupation = forms.CharField(required=False)
    institution = forms.CharField(required=False)
    phone = forms.CharField(required=False)
    email = forms.CharField(required=False)


class DescriptionForm(forms.Form):
    """Generic Description form for Extras and Skills Entries"""

    category_name = forms.CharField(label="Section", required=False)
    description = forms.CharField(
        label="",
        required=False,
        widget=forms.Textarea(
            attrs={"rows": 10, "cols": 60, "placeholder": "Extra data"}
        ),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Modify self.initial directly, since Django sets it automatically
        list_data = self.initial.get("description", [])

        if isinstance(list_data, list):
            self.initial["description"] = "\n".join(list_data)

    def clean_responsibilities(self):
        submited_list_data = self.cleaned_data.get("description", "")
        return submited_list_data.splitlines()


class ItemForm(forms.Form):
    item = forms.CharField(required=False, label="")
