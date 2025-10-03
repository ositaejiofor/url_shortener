from django.contrib import admin
from django.urls import path, include
from core import views  # or wherever you placed signup

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("stats/<str:code>/", views.stats, name="stats"),
    path("signup/", views.signup, name="signup"),  # 👈 add this before catch-all
    path("accounts/", include("django.contrib.auth.urls")),  # for login/logout
    path("<str:code>/", views.redirect_url, name="redirect_url"),  # keep last
]
