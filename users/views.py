from django.contrib.auth.views import LoginView
from django.forms import fields
from django.http.response import HttpResponseRedirect
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView, UpdateView

from users.models import Profile
from . import forms
from django.views import generic
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required


class UserCreateView(generic.CreateView):
    form_class = forms.RegisterForm
    template_name = 'users/register.html'
    success_url = '/'

class AuthUserView(LoginView):
    form_class = forms.AuthForm
    template_name = 'users/auth.html'
    success_url = '/'

class ProfileView(DetailView):
    model = User
    context_object_name = 'prfl'
    template_name = 'users/profile.html/'


@login_required
def edit_profile(request):
    if request.method == 'POST':
        user_form = forms.UpdateUserForm(instance=request.user, data=request.POST)
        profile_form = forms.UpdateProfileForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile_app:profile', request.user.id)
    else:
        user_form = forms.UpdateUserForm(instance=request.user)
        profile_form = forms.UpdateProfileForm(instance=request.user.profile)
        return render(request,
                      'users/edit_profile.html',
                      {'user_form': user_form,
                       'profile_form': profile_form})

