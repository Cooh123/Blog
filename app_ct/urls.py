from django.urls import path

from .views import CommentCreateView, DynamicCommentsLoad, AjaxDeleteView

urlpatterns = [
    path('create_comment/<str:content_type>/<int:object_id>/', CommentCreateView.as_view(), name='comment-create'),
    path('load_more_comments/', DynamicCommentsLoad.as_view(), name='load_more_comments'),
    path('delete_comment/', AjaxDeleteView.as_view(), name='delete_comment'),
]

app_name = 'app_ct'