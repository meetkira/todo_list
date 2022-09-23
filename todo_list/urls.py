from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView

urlpatterns = [
    path('admin/', admin.site.urls),

    path("oauth/", include("social_django.urls", namespace="social")),
    path("core/", include("core.urls")),
    path("goals/", include("goals.urls")),

    path("schema/", SpectacularAPIView.as_view(), name="schema")
]
