import os
from django.dispatch import receiver

from content.tasks import convert, delete_video_folder
from .models import Video
from django.db.models.signals import post_save, post_delete
import django_rq

@receiver(post_save, sender=Video)
def video_post_save(sender, instance, created, **kwargs):
    if(created):
        queue = django_rq.get_queue('default', autocommit=True)
        queue.enqueue(convert, instance.video_file.path, instance.title)


@receiver(post_delete, sender=Video)
def video_post_delete(sender, instance, **kwargs):
    if instance.video_file:
        base_folder = os.path.join('media', 'videos', instance.title.replace(" ", "_"))
        if os.path.exists(base_folder):
            delete_video_folder(base_folder)