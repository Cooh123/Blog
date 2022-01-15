"""Cooh URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


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
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)