from django.db import models
from django.core.validators import FileExtensionValidator

class ResumeModel(models.Model):
    pdf_file = models.FileField(
        upload_to='resumes/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])],
        blank=False,  # This prevents empty values in forms
        null=False  # Ensures database does not allow NULL
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)
