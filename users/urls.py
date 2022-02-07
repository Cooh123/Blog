
from email.mime import message
from unicodedata import name
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordChangeDoneView,
    PasswordChangeView
    )

from . import views 

app_name = 'profile_app'
urlpatterns = [
    path('reg/', views.UserCreateView.as_view(), name='reg'),
    path('auth', views.AuthUserView.as_view(), name='auth'),
    path('exit', LogoutView.as_view(template_name='users/exit.html'), name='exit'),
    path('profile/<int:pk>/', views.ProfileView.as_view(), name='profile'),
    path('profile/edit_profile/', views.edit_profile, name='update_profile'),
    path('password-change/', PasswordChangeView, name='password_change'),
    path('password-change/done/', PasswordChangeDoneView.as_view(template_name = 'users/password_change_done.html'), name='password_change_done'),
    path('add_subscribe/<int:pk>/', views.SubscribeToUser.as_view(), name='add_subscribe'),
    path('dialogs/<int:pk>/', views.DialogsDetail.as_view(), name='dialogs_user'),
    path('dialogs/', views.DialogsView.as_view(), name='dialogs'),
    path('create_message/', views.CreateMessageAjax.as_view(), name='create_message')
]
 
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)