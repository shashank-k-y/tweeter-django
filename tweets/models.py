from django.db import models

from profiles.models import User


class Tweet(models.Model):
    tweeter = models.ForeignKey(
        User, related_name="tweets", on_delete=models.CASCADE
    )
    text = models.TextField(max_length=1000)
    file = models.FileField(max_length=30)
    s3_key = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.tweeter.username
