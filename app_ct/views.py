from datetime import timedelta
import json
from django.shortcuts import render, get_object_or_404
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.views import View
from django.utils import timezone
from django.urls import reverse_lazy
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import DeleteView
from blog.models import Post

from .models import Comment
from .forms import CommentForm


class CommentCreateView(View):

    @staticmethod
    def post(request, *args, **kwargs):
        form = CommentForm(request.POST or None)
        ct = ContentType.objects.get(model=kwargs['content_type'])
        model = ct.model_class().objects.get(pk=kwargs['object_id'])
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.author = request.user
            new_comment.author_id = request.user.id
            new_comment.text = form.cleaned_data['text']
            new_comment.content_object = model
            new_comment.save()
            return HttpResponse(json.dumps({
                "id": new_comment.id,
                "text": new_comment.text,
                "author": str(new_comment.author),
                "author_id": int(new_comment.author_id),
                "created_at": str(new_comment.created_at.strftime("%Y-%m-%d %H:%M")), 
            }),
            content_type="application/json"
            )


class AjaxDeleteView(SingleObjectMixin, View):
    model = Comment

    @staticmethod
    def get(request, *args, **kwargs):
        comment_id =  request.GET.get('comment_id')
        user = request.GET.get('user')
        comment = Comment.objects.get(id=comment_id)
        if str(comment.author) == str(user):
            comment.delete()
            return JsonResponse({'data':'Комментарий удален успешно'})
        else:
            return JsonResponse({'data':'У вас нет прав'})


class DynamicCommentsLoad(View):

    @staticmethod
    def get(request, *args, **kwargs):
        last_comment_id = request.GET.get('lastCommentId')
        comment_object_id = request.GET.get('object_id')
        more_comments =  Comment.objects.filter(object_id=int(comment_object_id),pk__lt=int(last_comment_id))[:3]
        if not more_comments:
            return JsonResponse({'data': False})
        data = []
        for comment in more_comments:
            obj = {
                'id': comment.id,
                'object_id':comment.object_id,
                'text': comment.text,
                'created_at': str(comment.created_at.strftime("%Y-%m-%d %H:%M")),
                'author':str(comment.author),
                'img': comment.author.profile.img.url,
                'author_id': int(comment.author.id),
            }
            data.append(obj)
        data[-1]['last_comments'] = True
        return JsonResponse({'data': data})