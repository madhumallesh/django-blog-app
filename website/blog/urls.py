from django.urls import path

from .filter import blog_Filter
from . import views

urlpatterns = [
    path("", views.BlogView.as_view(), name="home"),
    path("view/<uuid:pk>/", views.UserBlogView.as_view(), name="view"),
    path("blog/<uuid:pk>/", views.BlogDetailView.as_view(), name="blog"),
    path("create/", views.BlogCreateView.as_view(), name="blog_create"),
    path("blog/<uuid:pk>/update", views.BlogUpdateView.as_view(), name="blog_update"),
    path("blog/<uuid:pk>/delete", views.BlogDeleteView.as_view(), name="blog-delete"),
]
