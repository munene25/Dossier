from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
import uuid

User = get_user_model()

class ResumeDataModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(default="My Resume", unique=False, max_length=50)
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
    created_at =  models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"Resume {self.id}"
    
