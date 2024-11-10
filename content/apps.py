from django.apps import AppConfig


class ContentConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "content"

    def ready(self):
        """
        This function sets the signals. It is needed to call the signals for the tasks like creating the new video resolution files, which then run in the background with an rq-worker.
        """
        from . import signals
