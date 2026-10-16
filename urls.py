from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from social import views

urlpatterns = [
 path("admin/", admin.site.urls), path("", views.feed, name="feed"),
 path("accounts/", include("django.contrib.auth.urls")),
 path("accounts/signup/", views.signup, name="signup"),
 path("post/new/", views.create_post, name="create_post"),
 path("post/<int:post_id>/like/", views.toggle_like, name="toggle_like"),
 path("post/<int:post_id>/comment/", views.add_comment, name="add_comment"),
 path("profile/edit/", views.edit_profile, name="edit_profile"),
 path("profile/<str:username>/", views.profile, name="profile"),
 path("follow/<str:username>/", views.toggle_follow, name="toggle_follow"),
 path("explore/", views.explore, name="explore"),
]
if settings.DEBUG:
 urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
