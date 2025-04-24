from django.urls import path
from . import views


app_name = "resumes"
urlpatterns = [
    path("", views.UploadView.as_view(), name="upload"),
    path(
        "modify/personal-information/<int:pk>",
        views.BasicFormView.as_view(category="personal_information"),
        name="personal_information",
    ),
    path(
        "modify/overview/<int:pk>",
        views.BasicFormView.as_view(category="overview"),
        name="overview",
    ),
    path(
        "modify/education/<int:pk>",
        views.FormsetView.as_view(category="education"),
        name="education",
    ),
    path(
        "modify/professional-experience/<int:pk>",
        views.FormsetView.as_view(category="professional_experience"),
        name="professional_experience",
    ),
    path(
        "modify/skills/<int:pk>",
        views.FormsetView.as_view(category="skills"),
        name="skills",
    ),
    path(
        "modify/referees/<int:pk>",
        views.FormsetView.as_view(category="referees"),
        name="referees",
    ),
    path(
        "modify/extras/<int:pk>",
        views.FormsetView.as_view(category="extras"),
        name="extras",
    ),
    path(
        "modify/certificates/<int:pk>",
        views.FormsetView.as_view(category="certificates"),
        name="certificates",
    ),
    path(
        "modify/languages/<int:pk>",
        views.FormsetView.as_view(category="languages"),
        name="languages",
    ),
    path(
        "render-resume/<int:pk>",
        views.render_resume,
        name="render_resume",
    ),
]
