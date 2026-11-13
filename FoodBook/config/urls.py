from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path

from catalog import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),
    path("register/", views.register, name="register"),
    path("add/", views.add_entry, name="add_entry"),
    path("login/", auth_views.LoginView.as_view(template_name="registration/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("edit/<int:entry_id>/", views.edit_entry, name="edit_entry"),
    path("delete/<int:entry_id>/", views.delete_entry, name="delete_entry"),
    path("lab/idor/insecure/<int:entry_id>/", views.idor_insecure_demo, name="idor_insecure"),
]
