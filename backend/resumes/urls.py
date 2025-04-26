from django.urls import path
from . import views


app_name = "resumes"
urlpatterns = [
    path("create/", views.create, name="create"),
    path("upload/", views.UploadView.as_view(), name="upload"),
    path("my-resumes/", views.ResumeListView.as_view(), name="my_resumes"),
    path("delete/<int:pk>", views.ResumeDeleteView.as_view(), name="delete"),
    path("select-resume/", views.select_resume, name="select_resume"),
    # path("sections/", views.ResumeListView.as_view(), name="modify"),
    path(
        "modify/personal-information/",
        views.BasicFormView.as_view(category="personal_information"),
        name="personal_information",
    ),
    path(
        "modify/overview/",
        views.BasicFormView.as_view(category="overview"),
        name="overview",
    ),
    path(
        "modify/education/",
        views.FormsetView.as_view(category="education"),
        name="education",
    ),
    path(
        "modify/professional-experience/",
        views.FormsetView.as_view(category="professional_experience"),
        name="professional_experience",
    ),
    path(
        "modify/skills/",
        views.FormsetView.as_view(category="skills"),
        name="skills",
    ),
    path(
        "modify/referees/",
        views.FormsetView.as_view(category="referees"),
        name="referees",
    ),
    path(
        "modify/extras/",
        views.FormsetView.as_view(category="extras"),
        name="extras",
    ),
    path(
        "modify/certificates/",
        views.FormsetView.as_view(category="certificates"),
        name="certificates",
    ),
    path(
        "modify/languages/",
        views.FormsetView.as_view(category="languages"),
        name="languages",
    ),
    path(
        "render-resume/",
        views.render_resume,
        name="render_resume",
    ),
]
