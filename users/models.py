from django.db import models
from django.contrib.auth.models import AbstractUser
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFit, ResizeToFill


class User(AbstractUser):
    photo = models.ImageField(upload_to="users/", null=True, blank=True)
    photo_thumb = ImageSpecField(source="photo", processors=[ResizeToFill(200,200)], format="JPEG", options={"quality":80})
    bio = models.CharField(max_length=200, null=True, blank=True)
