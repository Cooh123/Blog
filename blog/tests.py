from django.test import TestCase
from .models  import *
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

User =  get_user_model()

class BlogTestCases(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='testuser', password='password')
        self.post = Post.objects.create(name='Ноутбуки', slug='notebook')

