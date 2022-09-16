
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("save_post",views.save_post, name="save_post"),
    path("load",views.load_posts,name="load_posts"),
    path("load/followed",views.load_followed_posts,name="load_followed_posts"),
    path("profile/<int:user_id>",views.profile,name="profile"),
    path("profile/<int:profile_id>/update_follow",views.update_follow,name="update_follow"),
    path("post/<int:post_id>/update_like",views.update_like,name="update_like")
]
