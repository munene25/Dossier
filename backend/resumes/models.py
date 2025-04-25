from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class ResumeDataModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_defined_fields = models.JSONField()
    personal_information = models.JSONField()
    overview = models.JSONField()
    education = models.JSONField()
    professional_experience = models.JSONField()
    skills = models.JSONField()
    referees = models.JSONField()
    extras = models.JSONField()
    certificates = models.JSONField()
    languages = models.JSONField()
    
    def __str__(self):
        return f"Resume {self.id}"