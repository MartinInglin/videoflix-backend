import os
from django.dispatch import receiver

from content.tasks import convert, delete_videos
from .models import Video
from django.db.models.signals import post_save, post_delete
import django_rq

@receiver(post_save, sender=Video)
def video_post_save(sender, instance, created, **kwargs):
    if(created):
        queue = django_rq.get_queue('default', autocommit=True)
        queue.enqueue(convert, instance.video_file.path)


@receiver(post_delete, sender=Video)
def video_post_delete(sender, instance, **kwargs):
    if instance.video_file:
        file_path = instance.video_file.path
        if os.path.isfile(file_path):
            delete_videos(file_path)