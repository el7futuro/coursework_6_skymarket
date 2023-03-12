from django.conf import settings
from django.db import models
from users.models import User


class Ad(models.Model):
    title = models.CharField(max_length=100, null=True)
    price = models.PositiveIntegerField(null=True)
    description = models.CharField(max_length=2000, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='ads/', null=True, blank=True)

    class Meta:
        ordering = ['created_at']


class Comment(models.Model):
    text = models.CharField(max_length=2000, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    ad = models.ForeignKey(
        Ad,
        on_delete=models.CASCADE,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)