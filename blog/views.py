from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.generic.base import View
from django.views.generic.list import ListView

from .forms import CommentForm
from .models import Post


# Create your views here.
class HomeListView(ListView):
    template_name = "blog/home.html"
    model = Post
    context_object_name = "latest_posts"

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.order_by("date")[:3]
        return qs

class PostsListView(ListView):
    model = Post
    template_name = "blog/all-posts.html"
    context_object_name = "all_post"

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.order_by("date")

class PostDetailView(View):
    def is_stored_post(self, post_id):
        stored_posts = self.request.session.get("stored_posts")

        if stored_posts:
            is_stored = post_id in stored_posts
        else:
            is_stored = False

        return is_stored

    def get(self, request, slug):
        post_obj = get_object_or_404(Post, slug=slug)

        context = {
            "post" : post_obj,
            "is_stored" : self.is_stored_post(post_obj.id),
            "comments" : post_obj.comments.all().order_by("-id"),
            "post_tags" : post_obj.tags.all(),
            "comment_form" : CommentForm()
        }
        return render(request, "blog/post-detail.html", context)

    def post(self, request, slug):
        post_obj = get_object_or_404(Post, slug=slug)
        
        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post_obj
            comment.save()
            return HttpResponseRedirect(reverse("post-detail", args=[slug]))

        context = {
            "post" : post_obj,
            "is_stored" : self.is_stored_post(post_obj.id),
            "comments" : post_obj.comments.all().order_by("-id"),
            "post_tags" : post_obj.tags.all(),
            "comment_form" : CommentForm()
        } 
        return render(request, "blog/post-detail.html", context)


class ReadLaterView(View):
    def get(self, request):
        stored_posts = request.session.get("stored_posts")

        context = {}

        if stored_posts is None or len(stored_posts) == 0:
            context["posts"] = []
            context["has_post"] = False
        else:
            context["posts"] = Post.objects.filter(id__in=stored_posts)
            context["has_post"] = True

        return render(request, "blog/stored-posts.html", context)


    def post(self, request):
        stored_posts = request.session.get("stored_posts")

        if stored_posts is None:
            stored_posts = []
        
        post_id = int(request.POST.get("post_id"))

        if post_id not in stored_posts:
            stored_posts.append(post_id)
        else:
            stored_posts.remove(post_id)
        
        request.session["stored_posts"] = stored_posts

        return HttpResponseRedirect("/")
