from django.db import models


class Post(models.Model):
    """Модель поста"""
    company = models.CharField(max_length=100)
    link = models.SlugField(max_length=100)

class Comment(models.Model):
    """Модель комментариев"""
    comment_text = models.TextField()
    sender_username = models.CharField(max_length=100)
    sender_name = models.TextField(max_length=100)
    sender_phone=models.CharField(max_length=100,blank=True,null=True)
    date = models.DateTimeField()
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    polarity = models.CharField( default='Неизвестно', max_length=100)




