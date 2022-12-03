from django.shortcuts import render, HttpResponse, redirect

from django.views import generic, View
from django.views.generic.edit import FormMixin
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth.models import User
from django.contrib import auth, messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (
    LogoutView,
    LoginView,
    PasswordChangeView,
    PasswordChangeDoneView,
    PasswordResetView,
    PasswordResetConfirmView,
    PasswordResetDoneView,
    PasswordResetCompleteView,
)
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect, Http404
from django.core.mail import send_mail


from .forms import (
    RegisterForm,
    LoginForm,
    userForm,
    userProfile,
    userSettingForm,
    PasswordChangeForm,
    UserPasswordResetForm,
    UserSetPasswordForm,
)
from .models import UserSetting, UserProfileSetting

from blog.models import Posts
from .filter import UserPostsFilter

# Create your views here.
class LoginNotRequired:
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            raise Http404()
        return super().dispatch(request, *args, **kwargs)


class UserLoginView(LoginView):
    template_name: str = "users/sign-in.html"
    success_url = "/user"
    redirect_authenticated_user: bool = True

    def form_invalid(self, form) -> HttpResponse:
        form.add_error("password", "inavalid credentials")
        return super().form_invalid(form)


def UserLogoutView(request):
    if request.user.is_authenticated:
        auth.logout(request)
    return redirect("/user/login")


class UserPasswordResetView(LoginNotRequired, PasswordResetView):
    form_class = UserPasswordResetForm
    template_name: str = "users/password-reset.html"


class UserPasswordResetDoneView(LoginNotRequired, PasswordResetDoneView):
    template_name: str = "users/password-reset-done.html"
    # pass


class UserPasswordResetConfirmView(LoginNotRequired, PasswordResetConfirmView):
    form_class = UserSetPasswordForm
    template_name: str = "users/password-reset-set.html"
    success_url = reverse_lazy("password_reset_complete")


class UserPasswordResetCompleteView(LoginNotRequired, PasswordResetCompleteView):
    template_name: str = "users/password-reset-complete.html"


class UserPasswordChangeView(LoginRequiredMixin, generic.FormView):
    template_name: str = "users/password.html"
    form_class = PasswordChangeForm
    success_url = reverse_lazy("change-password-success")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    @csrf_exempt
    def form_valid(self, form) -> HttpResponse:
        print(form.cleaned_data)
        try:
            form.save()
            auth.update_session_auth_hash(self.request, self.request.user)
        except Exception:
            return self.form_invalid(form)
        return super().form_valid(form)

    def form_invalid(self, form) -> HttpResponse:
        print("form invalid")
        print(form.errors)
        return super().form_invalid(form)


class UserPasswordSuccess(LoginRequiredMixin, PasswordChangeDoneView):
    template_name = "users/password_success.html"


class ProfileView(LoginRequiredMixin, generic.TemplateView):
    login_url = "/user/login"
    template_name: str = "users/my-profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_setting"] = UserSetting.objects.filter(
            user=self.request.user
        ).all()
        query = Posts.objects.filter(author=self.request.user).all()
        filter_query = UserPostsFilter(self.request.GET, query)
        context["user_posts"] = filter_query.qs
        context["filter_form"] = filter_query.form
        return context


class SettingsView(LoginRequiredMixin, generic.TemplateView):
    login_url = "/user/login"
    template_name: str = "users/settings.html"
    user_form = userForm
    profile_form = userProfile
    user_settings = userSettingForm

    def get_success_url(self, **kwargs):
        return reverse("user-settings")

    def post(self, request):
        form = self.user_form(request.POST, instance=self.request.user)
        setting_form = self.user_settings(
            request.POST, instance=self.request.user.usersetting
        )
        profile_form = self.profile_form(
            request.POST, request.FILES, instance=self.request.user.userprofilesetting
        )

        if form.is_valid() and setting_form.is_valid():
            if form.has_changed():
                form.save()
                messages.success(
                    request, f"{form.changed_data} update successfully......."
                )
            if setting_form.has_changed():
                setting_form.instance.user = request.user
                setting_form.save()
                messages.success(
                    request, f"{setting_form.changed_data} update successfully......."
                )
                # print(setting_form.cleaned_data)
            if profile_form.has_changed():
                profile_form.instance.user = request.user
                profile_form.save()
                # print(profile_form.cleaned_data)
                messages.success(
                    request, f"{profile_form.changed_data} update successfully......."
                )
        return HttpResponseRedirect((self.get_success_url()))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_form"] = self.user_form(instance=self.request.user)

        context["user_setting"] = self.user_settings(
            instance=self.request.user.usersetting
        )
        # print(self.request.user.usersetting)

        context["user_profile"] = self.profile_form(
            instance=self.request.user.userprofilesetting
        )
        return context


class RegisterView(generic.edit.FormView):
    template_name: str = "users/sign-up.html"
    form_class = RegisterForm
    success_url = "/user/login"

    def get(self, request, *args, **kwargs) -> HttpResponse:
        if request.user.is_authenticated:
            return redirect("/user")
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        username = form.cleaned_data["username"]
        email = form.cleaned_data["email"]
        password = form.cleaned_data["conf_password"]
        try:
            user = User.objects.create_user(
                username=username, email=email, password=password
            )
            user.save()
            sett = UserSetting.objects.create(user=user)
            sett.save()
            prof = UserProfileSetting.objects.create(user=user)
            prof.save()
        except Exception as e:
            print(e)
            super().form_invalid(form)
        print("form valid ....")
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)
