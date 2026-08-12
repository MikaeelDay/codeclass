from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path(
        "",
        auth_views.LoginView.as_view(template_name="core/login.html"),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("run/", views.run_code, name="run_code"),
    path("submit/", views.save_submission, name="save_submission"),
    path("instructor/", views.instructor_overview, name="instructor_overview"),
    path("instructor/student/<int:user_id>/", views.instructor_student_detail, name="instructor_student_detail"),
]
