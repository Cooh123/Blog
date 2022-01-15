
import json

from django.shortcuts import  render
from .models import *
from app_ct.models import *
from app_ct.forms import CommentForm
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import auth
from django.http import  HttpResponse
from django.views import View




class LikeView(View):
    model = None
    def post(self, request, pk):
        obj = self.model.objects.get(pk=pk)
        like = LikeDislike.objects.get(object_id=obj.id)
        if request.user in like.like.all():
            like.like.remove(request.user)
        elif request.user in like.dis_like.all():
            like.dis_like.remove(request.user)
            like.like.add(request.user)
        else:
            like.like.add(request.user)
       
        return  HttpResponse(json.dumps({
            'like_count': like.like.all().count(),
            'dislike_count': like.dis_like.all().count(),
        }),
        content_type="application/json"
        )
    

class DislikeView(View):
    model = None
    def post(self, request, pk):
        obj = self.model.objects.get(pk=pk)
        like = LikeDislike.objects.get(object_id=obj.id)
        if request.user in like.like.all():
            like.like.remove(request.user)
            like.dis_like.add(request.user)
        elif request.user in like.dis_like.all():
            like.dis_like.remove(request.user)
        else:
            like.dis_like.add(request.user)
       
        return  HttpResponse(json.dumps({
            'like_count': like.like.all().count(),
            'dislike_count': like.dis_like.all().count(),
        }),
        content_type="application/json"
        )


class BookmarkView(View):
    model = None
 
    def post(self, request, pk):
        user = auth.get_user(request)
        bookmark, created = self.model.objects.get_or_create(user=user, obj_id=pk)
        if not created:
            bookmark.delete()
 
        return HttpResponse(
            json.dumps({
                "result": created,
                "count": self.model.objects.filter(obj_id=pk).count()
            }),
            content_type="application/json"
        )


def home(request):
    return render(request, 'blog/home.html')
    

class ShowPost(ListView):
    model = Post
    template_name = 'blog/blog.html'
    context_object_name = 'news'
    ordering = ['-date']


class CreatePost(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'blog/create_post.html'
    fields = ['title', 'topic', 'text']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class DetailPost(DetailView):
    model = Post
    context_object_name = 'post'
    def get_object(self):
        obj = super().get_object()
        obj.views += 1
        obj.save()
        return obj
    def get_context_data(self, **kwards):
        ctx = super(DetailPost, self).get_context_data(**kwards)
        ctx['form'] = CommentForm(self.request.POST or None)
        return ctx


class EditPost(UpdateView, LoginRequiredMixin, UserPassesTestMixin,):
    
    model = Post
    template_name = 'blog/edit_post.html'
    fields = ['title', 'text']
    success_url = '/blog/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True

        return False

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)   


class DeletePost(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/blog/'
    template_name = 'blog/delete_post.html'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True

        return False
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)   
   
    
# def get_client_ip(request):
#     x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
#     if x_forwarded_for:
#         ip = x_forwarded_for.split(',')[-1].strip()
#     else:
#         ip = request.META.get('REMOTE_ADDR')
#     return ip
   

     
