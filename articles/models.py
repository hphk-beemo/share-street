from django.db import models
from django.conf import settings


class Article(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(null=True, max_length=30)
    content = models.TextField(null=True)
    lat = models.FloatField(null=True)
    lng = models.FloatField(null=True)
    heading = models.FloatField(null=True)
    pitch = models.FloatField(null=True)
    thumbnail = models.ImageField(null=True, upload_to="articles/thumbnail")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
