from django.db import models


class ResumeDataModel(models.Model):
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