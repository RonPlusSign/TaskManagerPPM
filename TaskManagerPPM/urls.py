"""
URL configuration for TaskManagerPPM project.
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from . import views, settings

urlpatterns = [
    path("", views.HomepageView.as_view(), name="home"),
    path('admin/', admin.site.urls),
    path('lists/', include('lists.urls')),
    path("accounts/", include("accounts.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
