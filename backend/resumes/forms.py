from django import forms

class ResumeForm(forms.Form):
    pdf_file = forms.FileField(label='Upload Resume')

    def clean_pdf(self):
        file = self.cleaned_data.get('pdf_file') # pdf_file is how we stored it

        if file.content_type != 'applicationn/pdf':
            raise forms.ValidationError('Only PDF Files are Allowed')
        
        # We can check for file size later
        
        return file