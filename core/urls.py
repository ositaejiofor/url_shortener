from django.contrib import admin
from django.urls import path
from core import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path("admin/", admin.site.urls),

    # Core
    path("", views.home, name="home"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("stats/<str:code>/", views.stats, name="stats"),
    path("<str:code>/", views.redirect_url, name="redirect_url"),  # keep last

    # Auth
    path("signup/", views.signup, name="signup"),
    path("accounts/login/", auth_views.LoginView.as_view(template_name="registration/login.html"), name="login"),
    path(
        "accounts/logout/",
        LogoutView.as_view(next_page="/", http_method_names=["get", "post"]),
        name="logout",
    ),]
