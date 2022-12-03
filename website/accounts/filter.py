import django_filters
from django import forms

from blog.models import Posts


class UserPostsFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(field_name="title", lookup_expr="icontains")
    tag = django_filters.CharFilter(field_name="tag", lookup_expr="icontains")
    created_date = django_filters.DateFilter(
        field_name="created_date", lookup_expr="icontains"
    )

    class Meta:
        model = Posts
        fields = ["title", "tag", "created_date", "Status"]
        # ["title", "Status", "tag", "created_date"]
