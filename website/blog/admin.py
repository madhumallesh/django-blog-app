from django.contrib import admin
from .models import Posts, Comments, Tags

# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display = ("blog_id", "title", "created_date", "Status", "author")


class CommentAdmin(admin.ModelAdmin):
    list_display = ("name", "blog", "time")


admin.site.register(Posts, PostAdmin)
admin.site.register(Comments, CommentAdmin)
admin.site.register(Tags)
