from django.urls import path

from . import views

urlpatterns = [
    path("", views.HomeListView.as_view(extra_context={'title':'Home'}), name="home"),
    path("all-posts", views.PostsListView.as_view(), name="all-posts"),
    path("read-later", views.ReadLaterView.as_view(), name="read-later"),
    path("<slug:slug>", views.PostDetailView.as_view(), name="post-detail"),
]
