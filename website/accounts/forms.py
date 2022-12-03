from django import forms
from django.contrib.auth.models import User

from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib.auth.password_validation import validate_password

from .models import UserProfileSetting, UserSetting


class RegisterForm(forms.Form):
    username = forms.CharField(
        label="username",
        min_length=5,
        max_length=15,
        required=True,
        widget=forms.TextInput(),
    )
    email = forms.EmailField(
        max_length=30,
        label="email",
        min_length=10,
        required=True,
    )

    password = forms.CharField(
        label="password",
        min_length=5,
        max_length=10,
        required=True,
        widget=forms.PasswordInput(),
    )

    conf_password = forms.CharField(
        label="conf_password",
        min_length=5,
        max_length=10,
        required=True,
        widget=forms.PasswordInput(),
    )

    def clean_username(self):
        data = self.cleaned_data.get("username")
        if User.objects.filter(username=data).exists():
            raise forms.ValidationError("username already exists")
        return data

    def clean_email(self):
        data = self.cleaned_data.get("email")
        if User.objects.filter(email=data).exists():
            raise forms.ValidationError("email already exists")
        return data

    def clean_conf_password(self):
        pass1 = self.cleaned_data.get("conf_password")
        pass2 = self.cleaned_data.get("password")
        if pass1 != pass2:
            raise forms.ValidationError("password not matched")
        return pass1


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=30,
        label="username",
        min_length=5,
        required=True,
    )

    password = forms.CharField(
        label="password",
        min_length=5,
        max_length=10,
        required=True,
        widget=forms.PasswordInput(),
    )


class userForm(forms.ModelForm):
    username = forms.CharField(
        max_length=20,
        required=True,
        min_length=5,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    last_name = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={"class": "form-control"}),
        required=False,
    )
    first_name = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={"class": "form-control"}),
        required=False,
    )
    email = forms.EmailField(
        max_length=30, widget=forms.EmailInput(attrs={"class": "form-control"})
    )

    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name", "email"]


class userProfile(forms.ModelForm):
    profile_img = forms.ImageField(
        label="Profile",
        required=True,
        widget=forms.FileInput(
            attrs={"class": "form-control"},
        ),
    )
    background_img = forms.ImageField(
        required=False,
        label="Background Image",
        widget=forms.FileInput(attrs={"class": "form-control"}),
    )

    class Meta:
        model = UserProfileSetting
        fields = ["background_img", "profile_img"]


class userSettingForm(forms.ModelForm):
    Place = forms.CharField(
        label="Place",
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    birth_date = forms.DateField(
        label="Birth Date",
        required=False,
        widget=forms.DateInput(attrs={"class": "form-control", "type": "date"}),
    )
    status = forms.ChoiceField(
        choices=UserSetting.STATUS,
        label="status",
        required=False,
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    gender = forms.ChoiceField(
        choices=UserSetting.GENDER,
        required=False,
        label="Gender",
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    overview = forms.CharField(
        required=False,
        label="OverView",
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 4}),
    )

    class Meta:
        model = UserSetting
        fields = ["Place", "birth_date", "status", "gender", "overview"]


class PasswordChangeForm(forms.Form):

    old_password = forms.CharField(
        label="Current Password",
        min_length=5,
        max_length=10,
        required=False,
        widget=forms.PasswordInput(),
    )

    new_password1 = forms.CharField(
        label="New Password",
        min_length=5,
        max_length=10,
        required=False,
        widget=forms.PasswordInput(),
    )

    new_password2 = forms.CharField(
        label="Confirm Password",
        min_length=5,
        max_length=10,
        required=False,
        widget=forms.PasswordInput(),
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_old_password(self):
        password = self.cleaned_data.get("old_password")
        if not self.user.check_password(password):
            raise forms.ValidationError("You entered wrong password")
        return password

    def clean_new_password2(self):
        password = self.cleaned_data.get("old_password")
        pass1 = self.cleaned_data.get("new_password1")
        pass2 = self.cleaned_data.get("new_password2")
        print(self.user)
        if pass1 != pass2:
            raise forms.ValidationError("Password not matched")
        if pass1 == pass2 and pass2 == password:
            raise forms.ValidationError("password similar to the cuurent password")
        # validate_password(pass2)
        return pass1

    def save(self, commit=True):
        password = self.cleaned_data["new_password1"]
        self.user.set_password(password)
        if commit:
            self.user.save()
        return self.user


class UserPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(max_length=50, widget=forms.EmailInput)

    def clean_email(self):
        data = self.cleaned_data.get("email")
        if not User.objects.filter(email=data).values("email").exists():
            raise forms.ValidationError("This Email not exists...")
        return data


class UserSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label="New Password",
        min_length=5,
        max_length=10,
        required=False,
        widget=forms.PasswordInput(),
    )

    new_password2 = forms.CharField(
        label="Confirm Password",
        min_length=5,
        max_length=10,
        required=False,
        widget=forms.PasswordInput(),
    )

    def clean_new_password2(self) -> str:
        pass1 = self.cleaned_data.get("new_password1")
        pass2 = self.cleaned_data.get("new_password2")
        if pass1 != pass2:
            raise forms.ValidationError("Password not matched")
        return pass1
