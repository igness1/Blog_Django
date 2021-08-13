from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    path('',views.PostListView, name='post_list'),
    path('about/', views.About.as_view(), name='about'),
    path('post/new/',views.CreatePost.as_view(), name='new_post'),
    path('post/<int:pk>/', views.PostDetail.as_view(), name='post_detail'),
    path('post/<int:pk>/publish/',views.publish_post, name='publish_post'),
    path('post/<int:pk>/comment/', views.add_comment, name='add_comment'),
    path('post/<int:pk>/approve_comment/', views.approve_comment, name='comment_approve'),
    path('post/<int:pk>/remove_comment/', views.remove_comment, name='comment_remove'),
    path('post/<int:pk>/edit/', views.PostEdit.as_view(), name='edit_post'),
    path('post/<int:pk>/remove/', views.PostDelete.as_view(), name='remove_post'),
    path('like/<int:pk>/', views.give_like, name="give_like"),

]