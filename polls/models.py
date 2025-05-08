import datetime

from django import forms
from django.db import models
from django.utils import timezone
from django.shortcuts import get_object_or_404, render


# Create your models here.

class Post(models.Model):
    comment_flag = False
    post_title = models.CharField(max_length = 100)
    post_text = models.CharField(max_length = 800)
    pub_date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.post_title
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days =1)
    
class Comment(Post):
    comment_flag = True
    mother_post = models.ForeignKey(Post, on_delete = models.CASCADE, related_name='comments')

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['post_title','post_text']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields =['post_text']
        labels ={
            'post_text':'comment'
        }


# class Comment(models.Model):
#     question = models.ForeignKey(Post, on_delete = models.CASCADE)
#     choice_text = models.CharField(max_length = 200)
#     votes = models.IntegerField(default = 0)
#     def __str__(self):
#         return self.choice_text