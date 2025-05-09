# resumes/admin.py
from django.contrib import admin
from .models import ResumeDataModel # Import your model(s)

# Register your models here
admin.site.register(ResumeDataModel)
