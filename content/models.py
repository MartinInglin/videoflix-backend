import os
from datetime import date
from django.db import models

def video_upload_to(instance, filename):
    title_path = instance.title.replace(" ", "_")
    return os.path.join('videos', title_path, filename)

class Video(models.Model):
    created_at = models.DateField(default=date.today)
    title = models.CharField(max_length=80)
    description = models.CharField(max_length=500)
    video_file = models.FileField(upload_to=video_upload_to, blank=True, null=True)

    def __str__(self):
        return self.title
