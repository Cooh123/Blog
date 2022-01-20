from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.contenttypes.fields import  GenericRelation
from app_ct.models import *
from django.dispatch import receiver
from django.db.models.signals import post_save
from ckeditor.fields import RichTextField

from users.models import Profile
from app_ct.models import BookmarkBase


class Topic(models.Model):
    img = models.ImageField('Изображение темы', default='default.png', upload_to='topic_images')
    title = models.CharField('Название темы',max_length=15,unique=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Тема'
        verbose_name_plural = 'Темы'



class Post(models.Model):
    title = models.CharField(max_length=100,unique=True, verbose_name='Название статьи')
    text = RichTextField(blank=True,null=True, verbose_name='',config_name='create_post')
    date = models.DateTimeField(default=timezone.now, verbose_name='Дата публикации')
    author = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name='Автор статьи')
    topic =  models.ForeignKey(Topic,on_delete=models.CASCADE, verbose_name='Тема статьи')
    vote = GenericRelation(LikeDislike, related_query_name='like_posts', verbose_name='Лайки')
    comment = GenericRelation(Comment, related_query_name='comments_post', verbose_name='Комментарии')
    views = models.PositiveIntegerField(verbose_name='Просмотры', default=0)

    def like_count(self):
        return self.vote.all()[0].like.count()

    def dis_like_count(self):
        return self.vote.all()[0].dis_like.count()

    def get_absolute_url(self):
        return reverse('detail_post', kwargs={'pk': self.pk})
        
    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'

    def get_bookmark_count(self):
        return self.bookmarkpost_set.all().count()
    
    def bookmark_user_list(self):
        list_user =[]
        for i in self.bookmarkpost_set.all():
            list_user.append(i.user)
        return list_user

@receiver(post_save, sender=Post)
def create_like_objects(sender, instance, created, **kwargs):
    if created:
        LikeDislike.objects.create(content_object=instance)



class BookmarkPost(BookmarkBase):
    class Meta:
        db_table = "bookmark_article"
        verbose_name = 'Закладка'
        verbose_name_plural = 'Закладки'
 
    obj = models.ForeignKey(Post, verbose_name="Статья",on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    def get_bookmark_count(self):
        return self.bookmarkpost_set.all().count()

