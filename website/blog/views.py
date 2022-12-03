from django.shortcuts import render, HttpResponse, get_object_or_404
from django.views import generic, View
from django.http import HttpResponseRedirect
from django.urls import reverse, get_urlconf
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from django_filters.views import FilterView, FilterMixin

from .models import Posts, Comments, Tags
from .forms import CommentForm, BlogCreateForm

from .filter import blog_Filter


# Create your views here.


class UserBlogView(LoginRequiredMixin, generic.DetailView):
    model = Posts
    template_name: str = "users/post-view.html"
    query_pk_and_slug: bool = True
    context_object_name = "user_post"

    def get_object(self):
        post = get_object_or_404(
            self.model, blog_id=self.kwargs["pk"], author=self.request.user
        )
        return post


class BlogView(generic.ListView):
    template_name: str = "blogs/blog-list.html"
    model = Posts
    paginate_by: int = 5
    context_object_name = "blogs"
    filter = None

    def get_queryset(self):
        qs = super().get_queryset()
        if not cache.get("blogs_list"):
            cache.set(
                "blogs_list",
                (
                    qs.filter(Status="Publish")
                    .order_by("-created_date")
                    .select_related("author")
                ),
            )
        queryset = cache.get("blogs_list")

        data = self.request.GET
        self.filter = blog_Filter(data, queryset)
        return self.filter.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if not cache.get("recent_post"):
            cache.set(
                "recent_post",
                Posts.objects.filter(Status="Publish").order_by("-created_date")[:5],
            )
        x = cache.get("recent_post")

        context["recent_posts"] = x
        if not cache.get("Tags"):
            cache.set("Tags", Tags.objects.all())

        context["tags"] = cache.get("Tags")
        context["search_form"] = self.filter.form
        return context


class BlogDetailView(generic.edit.FormMixin, generic.DetailView):
    model = Posts
    template_name: str = "blogs/blog-detail.html"
    context_object_name = "blog"
    # queryset = model.objects.filter(Status="Publish").select_related("author")
    form_class = CommentForm
    get_blog = None

    def get_object(self):
        self.get_blog = get_object_or_404(
            Posts, blog_id=self.kwargs["pk"], Status="Publish"
        )
        return self.get_blog

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comments"] = self.get_blog.comments_set.all()
        return context

    def post(self, *args, **kwargs):
        pk = self.kwargs["pk"]
        # print(pk)
        form = self.get_form()
        if form.is_valid():
            blog_id = get_object_or_404(self.model, blog_id=pk)
            form.save(commit=False)
            form.instance.blog = blog_id
            form.save(commit=True)
            # print(form.cleaned_data)
        return HttpResponseRedirect(reverse("blog", args=(pk,)))


class BlogCreateView(LoginRequiredMixin, generic.CreateView):
    form_class = BlogCreateForm
    template_name: str = "blogs/blog_create.html"
    success_url = "/user"

    def form_valid(self, form) -> HttpResponse:
        try:
            form.instance.author = self.request.user
            form.save()
        except Exception as e:
            print(e)
            return self.form_invalid(form)
        return super().form_valid(form)

    def form_invalid(self, form) -> HttpResponse:
        print(form.cleaned_data)
        print("form invalid")
        # print(form.cleaned_data)
        return super().form_invalid(form)


class BlogUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name: str = "blogs/blog_update.html"
    model = Posts
    fields = ["title", "post_image", "tag", "Status", "content"]
    # form_class = BlogUpdateForm
    success_url = "/user"

    def get_queryset(self):
        print(self.kwargs["pk"])
        return Posts.objects.filter(blog_id=self.kwargs["pk"], author=self.request.user)

    def form_valid(self, form) -> HttpResponse:
        print(form.cleaned_data)
        if form.has_changed():
            print(form.changed_data)
            form.save()
            messages.success(self.request, f" {form.changed_data} Update sucessfully")
        return HttpResponseRedirect(reverse("blog_update", args=(self.kwargs["pk"],)))


class BlogDeleteView(LoginRequiredMixin, generic.DeleteView):
    template_name: str = "blogs/blog_delete.html"
    model = Posts
    success_url = get_urlconf("/user")

    def get_queryset(self):
        return Posts.objects.filter(author=self.request.user, blog_id=self.kwargs["pk"])
