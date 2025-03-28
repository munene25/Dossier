from django.db import models


class ResumeDataModel(models.Model):
    user_defined_fields = models.JSONField(default=dict)
    personal_information = models.JSONField(default=dict)
    overview = models.JSONField(default=dict)
    education = models.JSONField(default=list)
    professional_experience = models.JSONField(default=list)
    skills = models.JSONField(default=list)
    referees = models.JSONField(default=list)
    extras = models.JSONField(default=list)
    certificates = models.JSONField(default=list)
    languages = models.JSONField(default=list)
    
    def __str__(self):
        return f"Resume {self.id}"