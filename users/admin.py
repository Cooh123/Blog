from django.contrib import admin
from django.contrib.auth.models import User
from .models import Message, Profile, BookmarkUser, Chat


admin.site.register(Profile)
admin.site.register(BookmarkUser)
admin.site.register(Message)
admin.site.register(Chat)

