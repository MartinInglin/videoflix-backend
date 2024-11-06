"""
URL configuration for videoflix_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.views.generic.base import RedirectView
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from debug_toolbar.toolbar import debug_toolbar_urls
from authentication.views import (
    CustomLoginView,
    ForgotPassword,
    LogoutView,
    RegistrationView,
    ResendVerificationEmail,
    ResetPassword,
    VerificationView,
)

from content.views import DashboardView, HeroView
from watch_history.views import GetWatchHistory, UpdateWatchHistory

urlpatterns = (
    [
        path("", RedirectView.as_view(url="/admin/", permanent=True), name="index"),
        path("admin/", admin.site.urls),
        path("django-rq/", include("django_rq.urls")),
        path("registration/", RegistrationView.as_view(), name="registration"),
        path("verification/", VerificationView.as_view(), name="verification"),
        path(
            "resend_verifiction/",
            ResendVerificationEmail.as_view(),
            name="resend_verification",
        ),
        path("forgot_password/", ForgotPassword.as_view(), name="forgot_password"),
        path("reset_password/", ResetPassword.as_view(), name="reset_password"),
        path("login/", CustomLoginView.as_view(), name="login"),
        path("logout/", LogoutView.as_view(), name="logout"),
        path("dashboard/", DashboardView.as_view(), name="dashboard"),
        path("hero/", HeroView.as_view(), name="hero"),

        path('update_watch_history/', UpdateWatchHistory.as_view(), name='update_watch_history'),
    ]
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    + debug_toolbar_urls()
)
