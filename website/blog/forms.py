from django import forms
from .models import Comments, Posts

from ckeditor.widgets import CKEditorWidget


class CommentForm(forms.ModelForm):
    name = forms.CharField(
        label="Name",
        required=True,
        min_length=5,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    email = forms.EmailField(
        label="Email",
        required=True,
        min_length=5,
        widget=forms.EmailInput(attrs={"class": "form-control"}),
    )
    comment = forms.CharField(
        label="Comment",
        required=True,
        min_length=5,
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 4}),
    )

    class Meta:
        model = Comments
        fields = ["name", "email", "comment"]


class BlogCreateForm(forms.ModelForm):
    content = forms.CharField(
        label="content",
        widget=CKEditorWidget(),
    )
    title = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"}),
        min_length=5,
        max_length=50,
        required=True,
    )

    tag = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control", "list": "tags"}),
        required=True,
        max_length=25,
        min_length=5,
    )

    post_image = forms.ImageField(
        label="post_image",
        required=True,
        widget=forms.FileInput(
            attrs={"class": "form-control"},
        ),
    )

    Status = forms.ChoiceField(
        choices=Posts.STATUS,
        label="status",
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    class Meta:
        model = Posts
        fields = ["title", "tag", "Status", "content", "post_image"]

    def clean_title(self):
        data = self.cleaned_data.get("title")
        if Posts.objects.filter(title=data).exists():
            raise forms.ValidationError("the name is already exists")
        return data
