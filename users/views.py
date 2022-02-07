from django import template
from django.db.models import Count, Max
from django.contrib.auth.views import LoginView
from django.http.response import HttpResponseRedirect
from django.http import  JsonResponse, HttpResponse
from django.views.generic import ListView,TemplateView, CreateView
from django.views.generic.detail import DetailView
from users.models import Chat, Message, BookmarkUser
from users.templatetags.all_messages import all_messages
from . import forms
from django.views import generic, View
from django.views.generic.edit import FormView
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
import json


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


class SubscribeToUser(View):
    model = User
    def get(self, request, pk):
        obj = self.model.objects.get(pk=pk)
        if list(BookmarkUser.objects.filter(user=request.user, who_added=obj)) == []:
            BookmarkUser.objects.create(user=request.user, who_added=obj)
        else:
            BookmarkUser.objects.get(user=request.user, who_added=obj).delete()
        return HttpResponseRedirect('/profile/%a'%pk)


# class MessageUserView(DetailView):
#     model = Chat
#     context_object_name = 'chats'
#     template_name = 'users/message.html'


class DialogsView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'users/login_error.html')
        else:
            all_messages = Chat.objects.filter(
                members__in=[request.user]
                ).annotate(
                count=Count('message')
                ).filter(
                count__gt=0
                ).annotate(
                last_message_pub_date=Max('message__pub_date')
                ).order_by('-last_message_pub_date')
            return render(request, 'users/dialogs.html', {'all_messages': all_messages}) 
class CreateMessageAjax(View):
    @staticmethod
    def post(request, *args, **kwargs):
        id_chat = int(request.POST.get('id_chat'))
        text = request.POST.get('text')
        chat = Chat.objects.get(id=id_chat)
        if text != '':
            message = Message.objects.create(chat=chat, author=request.user, message=text)
        return HttpResponse(
            json.dumps({
                "text": text,
                'pub_date': 'только что' 
            }),
            content_type="application/json"
            )

class DialogsDetail(View):
    def get(self, request, pk):
        if not request.user.is_authenticated:
            return render(request, 'users/login_error.html')
        else:
            user = User.objects.get(id=pk)
            if len(request.user.chat_set.filter(members__in=[request.user]).filter(members__in=[user])) != 1:
                chat = Chat.objects.create()
                chat.members.add(request.user)
                chat.members.add(user)
            chat = request.user.chat_set.filter(members__in=[request.user]).filter(members__in=[user])
            all_messages = Chat.objects.filter(
                members__in=[request.user]
                ).annotate(
                count=Count('message')
                ).filter(
                count__gt=0
                ).annotate(
                last_message_pub_date=Max('message__pub_date')
                ).order_by('-last_message_pub_date')
            for message in chat[0].message_set.filter(is_readed=False).exclude(author=request.user):
                message.is_readed = True
                message.save()
            
            return render(request, 'users/detail_dialogs.html', {'chat': chat[0], 'all_massages': all_messages} ) 

