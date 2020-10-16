from django.db import models
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill, ResizeToFit
from users.models import User

class Route(models.Model):
    mountainproject_id = models.CharField(max_length=100, null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    route_type = models.CharField(max_length=100, null=True, blank=True)
    rating = models.CharField(max_length=100, null=True, blank=True)
    mp_stars = models.IntegerField()
    pitches = models.CharField(max_length=100, null=True, blank=True)
    location = models.TextField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateField(auto_now=True)
    

class Daytrip(models.Model):
    title = models.CharField(max_length=100, null=False, blank=False)
    description = models.CharField(max_length=200, null=True, blank=True)
    owners = models.ManyToManyField(to=User, related_name="daytrips", blank=True)
    routes = models.ManyToManyField(to=Route, related_name="daytrips", blank=True)
    date = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)
    date_added = models.DateField(auto_now_add=True)
    date_updated = models.DateField(auto_now=True)


class Log(models.Model):
    text = models.TextField(null=False, blank=False)
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="logs", null=True, blank=True)
    daytrip = models.ForeignKey(to=Daytrip, on_delete=models.CASCADE, related_name="logs", null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    text = models.TextField(null=False, blank=False)
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="comments", null=True, blank=True)
    route = models.ForeignKey(to=Route, on_delete=models.CASCADE, related_name="comments", null=True, blank=True)
    point_of_interest = models.ForeignKey(to=Pointofinterest, on_delete=models.CASCADE, related_name="comments", null=True, blank=True)


class Star(models.Model):
    stars = models.IntegerField()
    route = models.ForeignKey(to=Route, on_delete=models.CASCADE, related_name="stars", null=True, blank=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="stars", null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)


class Photo(models.Model):
    photo = models.ImageField(upload_to="routephotos/", null=True, blank=True)
    photo_thumb = ImageSpecField(source="photo", processors=[ResizeToFill(200,200)], format="JPEG", options={"quality": 80})
    photo_large = ImageSpecField(source="photo", processors=[ResizeToFit(400,400)], format="JPEG", options={"quality": 80})
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="photos", null=True, blank=True)
    route = models.ForeignKey(to=Route, on_delete=models.CASCADE, related_name="photos", null=True, blank=True)
    description = models.CharField(max_length=200, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)


class Pointofinterest(models.Model):
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="pointsofinterest", null=True, blank=True)
    title = models.CharField(max_length=100, null=False, blank=False)
    description = models.CharField(max_length=200, null=True, blank=True)
    longitude = models.FloatField(null=False, blank=False)
    latitude = models.FloatField(null=False, blank=False)
    date_added = models.DateField(auto_now_add=True)
    date_updated = models.DateField(auto_now=True)
    public = models.BooleanField(default=True)
    HANGOUT = "HG"
    PARKING = "PG"
    TRAILHEAD = "TH"
    CATEGORY_CHOICES = [
        (HANGOUT, "Hangout Spot"),
        (PARKING, "Parking"),
        (TRAILHEAD, "Trailhead"),
    ]
    category = models.CharField(max_length=2, choices=CATEGORY_CHOICES, default=HANGOUT)


