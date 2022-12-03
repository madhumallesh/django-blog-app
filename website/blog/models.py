from django.db import models
import uuid
from django.contrib.auth.models import User

from ckeditor_uploader.fields import RichTextUploadingField
from ckeditor.fields import RichTextField

# Create your models here.


class Posts(models.Model):
    STATUS = (
        ("Draft", "Draft"),
        ("Publish", "Publish"),
        ("Private", "Private"),
    )
    author = models.ForeignKey(to=User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    blog_id = models.CharField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        primary_key=True,
        max_length=50,
    )
    created_date = models.DateTimeField(auto_now_add=True, editable=False)
    last_modified_date = models.DateTimeField(auto_now=True, editable=False)
    post_image = models.ImageField(upload_to="blogs", null=True)
    content = RichTextField(blank=True)
    tag = models.CharField(max_length=50)
    Status = models.CharField(max_length=30, choices=STATUS, default="Private")

    def __str__(self) -> str:
        return f"{self.blog_id} -> {self.title}"

    class Meta:
        db_table = "blog_Posts"
        managed = True
        verbose_name = "Post"
        verbose_name_plural = "Posts"


class Comments(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    comment = models.TextField()
    time = models.DateTimeField(auto_now=True)
    blog = models.ForeignKey(to=Posts, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.name} -> {self.blog}"

    class Meta:
        ordering = ("-time",)


class Tags(models.Model):
    tagname = models.CharField(max_length=50, unique=True, null=False)

    def __str__(self) -> str:
        return self.tagname

    class Meta:
        db_table = "blog_tags"
        managed = True
        verbose_name = "Tags"
        verbose_name_plural = "Tagss"
