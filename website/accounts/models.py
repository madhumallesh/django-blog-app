import os
from django.db import models
from django.contrib.auth.models import User
import uuid


class UserProfileSetting(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    background_img = models.ImageField(upload_to="Back", null=True)
    profile_img = models.ImageField(
        upload_to="Profile", default="Profile/placeholder.jpg"
    )

    def __str__(self) -> str:
        return self.user.username

    class Meta:
        db_table = "User_Profile"
        managed = True
        verbose_name = "user profile"
        verbose_name_plural = "user profiles"


class UserSetting(models.Model):
    GENDER = (
        ("male", "Male"),
        ("female", "Female"),
    )
    STATUS = (
        ("Single", "Single"),
        ("Maried", "Maried"),
        ("UnMaried", "UnMaried"),
    )
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    Place = models.CharField(max_length=125, null=True)
    birth_date = models.DateField(null=True)
    status = models.CharField(max_length=50, null=True)
    gender = models.CharField(max_length=30, choices=GENDER)
    overview = models.TextField()

    def __str__(self) -> str:
        return self.user.username

    class Meta:
        db_table = "User_settings"
        managed = True
        verbose_name = "user settings"
        verbose_name_plural = "user settingss"


class Notification(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    content = models.TextField(max_length=125)
    url = models.CharField(max_length=125, null=True, default=None)
    time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "user_Notification"
        managed = True
        verbose_name = "user_Notification"
        verbose_name_plural = "user_Notifications"
        ordering = ("-time",)

    def __str__(self) -> str:
        return f"{self.user} {self.content}"
