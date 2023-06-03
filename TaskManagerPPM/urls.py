"""
URL configuration for TaskManagerPPM project.
"""
from django.contrib import admin
from django.urls import include, path

from . import views

urlpatterns = [
    path("", views.HomepageView.as_view(), name="home"),
    path('admin/', admin.site.urls),
    path('tasks/', include('tasks.urls')),
    path("accounts/", include("accounts.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
]
