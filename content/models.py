import os
from datetime import date
from django.db import models

def video_upload_to(instance, filename):
    title_path = instance.title.replace(" ", "_")
    return os.path.join('videos', title_path, filename)

def thumbnail_upload_to(instance, filename):
    title_path = instance.title.replace(" ", "_")
    return os.path.join('thumbnails', title_path, filename)

class Video(models.Model):
    CATEGORY_CHOICES = [
        ('documentary', 'Documentary'),
        ('drama', 'Drama'),
        ('romance', 'Romance'),
    ]
    created_at = models.DateField(default=date.today)
    title = models.CharField(max_length=80)
    description = models.CharField(max_length=500)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, blank=True, null=True)
    thumbnail = models.ImageField(upload_to=thumbnail_upload_to, blank=True, null=True)
    teaser = models.FileField(upload_to=video_upload_to, blank=True, null=True)
    video_file = models.FileField(upload_to=video_upload_to, blank=True, null=True)
    hls_file_360 = models.FileField(max_length=255, blank=True, null=True)
    hls_file_480 = models.FileField(max_length=255, blank=True, null=True)
    hls_file_720 = models.FileField(max_length=255, blank=True, null=True)
    hls_file_1080 = models.FileField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.title
