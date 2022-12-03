from django.contrib import admin
from . import models


# Register your models here.
admin.site.register(models.UserProfileSetting)
admin.site.register(models.UserSetting)
admin.site.register(models.Notification)
