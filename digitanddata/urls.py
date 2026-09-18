"""
URL configuration for digitanddata project.
"""
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('mathematics/', include('mathematics.urls')),
    path('computer-science/', include('computer_science.urls')),
    path('blog/', include('blog.urls')),
    path('accounts/', include('accounts.urls')),
    path('', include('leads.urls')),
    path('', include('core.urls')),
]
