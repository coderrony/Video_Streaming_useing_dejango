from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Category(models.Model):
    category_name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.category_name


class UploadContent(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_upload")
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="user_category")
    video_urls = models.URLField()
    slug = models.SlugField(blank=True)
    video_title = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.video_title


class Comment(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_comment")
    content = models.ForeignKey(
        UploadContent, on_delete=models.CASCADE, related_name="user_content")
    comment_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.comment_text
