from app_ct.models import Comment
from django import forms

class CommentForm(forms.ModelForm):
    class Meta:
        fields = ['text']
        model = Comment
