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