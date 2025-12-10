"""
URL configuration for gradinaCraciun project.
"""

from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

from gradinaCraciun import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # Store app URLs
    path('', include('store.urls')),  # main store routes

    # Authentication
    path('accounts/', include("django.contrib.auth.urls")),

    # Home page fallback
    path("", TemplateView.as_view(template_name="product_list.html"), name="product_list"),
]

# Serve media files
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
