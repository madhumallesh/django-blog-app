from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.UserLoginView.as_view(), name="login"),
    path("signup", views.RegisterView.as_view(), name="register"),
    path("", views.ProfileView.as_view(), name="user"),
    path("setting", views.SettingsView.as_view(), name="user-settings"),
    path("logout", views.UserLogoutView, name="logout"),
    path(
        "change-password",
        views.UserPasswordChangeView.as_view(),
        name="change-password",
    ),
    path(
        "password-change-success",
        views.UserPasswordSuccess.as_view(),
        name="change-password-success",
    ),
    path(
        "password-reset", views.UserPasswordResetView.as_view(), name="password-reset"
    ),
    path(
        "password-reset-confirm/<uidb64>/<token>/",
        views.UserPasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "password-reset-done",
        views.UserPasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "password-reset-complete",
        views.UserPasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
]
