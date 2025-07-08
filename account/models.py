from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser): 
    role = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Follow(models.Model): 
    follower = models.ForeignKey(
        User, related_name="following_set", on_delete=models.CASCADE
    )
    following = models.ForeignKey(
        User, related_name="follower_set", on_delete=models.CASCADE
    )

    class Meta:
        unique_together = ("follower", "following")

