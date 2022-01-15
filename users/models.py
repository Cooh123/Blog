from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.contenttypes.fields import  GenericRelation



from app_ct.models import Comment

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField('О себе',max_length=1000, default='')
    mobile_number = models.CharField('Мобильный номер',max_length=15, default='')
    img = models.ImageField('Фото пользователя', default='default.png', upload_to='user_images')

    def all_bookmarks(self):
        return self.user.bookmarkpost_set.all()[0:]
    
    def all_comments(self):
        return self.user.comment_set.all()[0:5]

    def all_post(self):
        return self.user.post_set.all()[0:5]

    def like_count(self):
        like_count =  self.user.like.count()
        return like_count 

    def all_like(self):
        like_set = self.user.like.all()
        return like_set
        
    def dis_like_count(self):
        dis_like_count =  self.user.dis_like.count()
        return dis_like_count 

    def all_dis_like(self):
        dis_like_set = self.user.dis_like.all()
        return dis_like_set

    def comment_all(self):
        return self.user.comment_set.all()

    def save(self, *args, **kwargs):
        # delete old file when replacing by updating the file
        try:
            this = Profile.objects.get(id=self.id)
            if this.img != self.img:
                this.img.delete(save=False)
        except: pass # when new photo then we do nothing, normal case          
        super(Profile, self).save(*args, **kwargs)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()