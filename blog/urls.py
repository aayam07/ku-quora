from django.urls import path
from . import views

urlpatterns = [
    path('',views.index_view,name='home'),
    path('create_post/',views.create_post_view,name='create_post'),
    path('<uuid:post_id>/',views.post_detail_view,name='post_detail'),
    path('like/',views.like_post_view,name='like_post'),
    path('dislike/',views.dislike_post_view,name='dislike_post'),
    path('tag/<slug:tag_slug>',views.tags_post_view,name='tags'),
]