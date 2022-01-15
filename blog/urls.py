from django.urls import path
from blog import models
from . import views 


urlpatterns = [
    path('', views.home, name='home'),
    path('blog/', views.ShowPost.as_view(), name='blog'),
    path('blog/create_post/', views.CreatePost.as_view(), name='create_post'),
    path('blog/<int:pk>/', views.DetailPost.as_view(), name='detail_post'),
    path('blog/<int:pk>/edit/', views.EditPost.as_view(), name='edit_post'),
    path('blog/<int:pk>/delete/', views.DeletePost.as_view(), name='delete_post'),
    path('like/<int:pk>/', views.LikeView.as_view(model=models.Post), name='like_post'),
    path('dis_like/<int:pk>/', views.DislikeView.as_view(model=models.Post), name='dislike_post'),
    path('blog/<int:pk>/bookmarks/', views.BookmarkView.as_view(model=models.BookmarkPost), name='post_bookmarks')
   ]
