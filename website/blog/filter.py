import django_filters
from .models import Posts


class blog_Filter(django_filters.FilterSet):
    tag = django_filters.CharFilter(field_name="tag", lookup_expr="icontains")
    title = django_filters.CharFilter(field_name="title", lookup_expr="icontains")

    class Meta:
        model = Posts
        fields = ["tag", "author", "title", "created_date"]
