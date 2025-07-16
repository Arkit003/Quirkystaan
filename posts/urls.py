from django.urls import path
from . import views

urlpatterns = [
    path("post_create/",views.post_creation,name="post_creation"),
    path("feed",views.feed,name='feed'),
    path('like',views.like_post,name='like')
]