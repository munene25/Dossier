from django.db import models
from django.core.validators import FileExtensionValidator

class ResumeModel(models.Model):
    file = models.FileField(
        upload_to='resumes/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])],
        blank=False,  # This prevents empty values in forms
        null=False  # Ensures database   not allow NULL
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)


class DataModel(models.Model):
    resume_model = models.OneToOneField(ResumeModel, on_delete=models.CASCADE, related_name='data_model')
    user_defined_fields = models.JSONField(default=dict)
    personal_information = models.JSONField(default=dict)
    overview = models.JSONField(default=dict)
    professional_experience = models.JSONField(default=list)
    education = models.JSONField(default=list)
    skills = models.JSONField(default=dict)
    referees = models.JSONField(default=list)
    extras = models.JSONField(default=list)
    certificates = models.JSONField(default=list)
    languages = models.JSONField(default=list)