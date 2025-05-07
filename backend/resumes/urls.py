from django.urls import path
from . import views


app_name = "resumes"
urlpatterns = [
    path("create/", views.CreateView.as_view(), name="create"),
    path("upload/", views.UploadView.as_view(), name="upload"),
    path("my-resumes/", views.ResumeListView.as_view(), name="my_resumes"),
    path("delete/<uuid:resume_id>", views.ResumeDeleteView.as_view(), name="delete"),
    path("preview/<uuid:resume_id>", views.ResumePreviewView.as_view(), name="preview"),
    path("download/<uuid:resume_id>", views.DownloadView.as_view(), name="download"),
    path(
        "modify/personal-information/<uuid:resume_id>",
        views.BasicFormView.as_view(category="personal_information"),
        name="personal_information",
    ),
    path(
        "modify/overview/<uuid:resume_id>",
        views.BasicFormView.as_view(category="overview"),
        name="overview",
    ),
    path(
        "modify/education/<uuid:resume_id>",
        views.FormsetView.as_view(category="education"),
        name="education",
    ),
    path(
        "modify/professional-experience/<uuid:resume_id>",
        views.FormsetView.as_view(category="professional_experience"),
        name="professional_experience",
    ),
    path(
        "modify/skills/<uuid:resume_id>",
        views.FormsetView.as_view(category="skills"),
        name="skills",
    ),
    path(
        "modify/referees/<uuid:resume_id>",
        views.FormsetView.as_view(category="referees"),
        name="referees",
    ),
    path(
        "modify/extras/<uuid:resume_id>",
        views.FormsetView.as_view(category="extras"),
        name="extras",
    ),
    path(
        "modify/certificates/<uuid:resume_id>",
        views.FormsetView.as_view(category="certificates"),
        name="certificates",
    ),
    path(
        "modify/languages/<uuid:resume_id>",
        views.FormsetView.as_view(category="languages"),
        name="languages",
    ),
]
