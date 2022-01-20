from django.db import models
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField

class CustomDateTimeField(models.DateTimeField):
    def value_to_string(self, obj):
        val = self.value_from_object(obj)
        if val:
            val.replace(microsecond=0)
            return val.isoformat()
        return ''

class LikeDislike(models.Model):
    like = models.ManyToManyField(User,related_name='like')
    dis_like =  models.ManyToManyField(User, related_name='dis_like')

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    def __str__(self) -> str:
        return f'{self.content_object}'
    class  Meta:
        verbose_name = 'Лайки'
        verbose_name_plural = 'Лайки'
    

class Comment(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    text = RichTextField(blank=True,null=True,verbose_name='',config_name='create_comment')
    created_at = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, verbose_name='Автор комментария', on_delete=models.CASCADE)


    def __str__(self):
        return f'{self.content_object}'
    
    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-created_at']
        
        
        
    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = timezone.now()
        super().save(*args, **kwargs)


class BookmarkBase(models.Model):
    class Meta:
        abstract = True
 
    user = models.ForeignKey(User, verbose_name="Пользователь",on_delete=models.CASCADE)
 
    def __str__(self):
        return self.user.username

 
