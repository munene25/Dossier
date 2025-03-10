from django import forms
from .models import ResumeModel

class ResumeForm(forms.ModelForm):
    class Meta:
        model = ResumeModel
        fields = ['file']
        labels = {'file': "Upload Your Resume (PDF Only)"}

    def clean_pdf_file(self):
        file = self.cleaned_data['pdf_file'] # pdf_file is how we stored it
        if file.content_type != 'application/pdf':
            raise forms.ValidationError('Only PDF Files are Allowed')

        # We can check for file size later
        return file
    
    
class PersonalInformationForm(forms.Form):
    UserDefinedField = forms.CharField(
            label="",
            widget = forms.TextInput(attrs={'placeholder': 'Category', 'id': 'category'}),
            required=False
        )
    Name = forms.CharField(required=False)
    Phone = forms.CharField(required=False)
    Email = forms.CharField(required=False)
    LinkedIn = forms.CharField(required=False)
    ExternalLink = forms.CharField(
            label="External link or Porfolio",
            widget = forms.TextInput(attrs={'placeholder': 'portfolio.com'}),
            required=False
        )
    
class OverviewForm(forms.Form):
    UserDefinedField = forms.CharField(
            label="",
            widget = forms.TextInput(attrs={'placeholder': 'Category', 'id': 'category'}),
            required=False
        )
    Text = forms.CharField(
            label='',
            required=False,
            widget=forms.Textarea(attrs={'placeholder': 'Brief Summary of yourself, work-experience, education and related data'}),
        )
# class Overview(forms.Form):
#     UserDefinedField = forms.CharField(
#             label="",
#             widget = forms.TextInput(attrs={'placeholder': 'Category', 'id': 'category'}),
#             required=False
#         )
# class Overview(forms.Form):
#     UserDefinedField = forms.CharField(
#             label="",
#             widget = forms.TextInput(attrs={'placeholder': 'Category', 'id': 'category'}),
#             required=False
#         )