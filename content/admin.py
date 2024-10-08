from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Video

class VideoResource(resources.ModelResource):

    class Meta:
        model = Video

@admin.register(Video)
class VideoAdmin(ImportExportModelAdmin):
    def get_fields(self, request, obj=None):
        # When adding a new video, exclude HLS file fields
        if obj is None:  # Add form
            return ['title', 'created_at', 'description', 'video_file']
        else:  # Edit form
            return ['title', 'created_at', 'description', 'video_file', 'hls_file_360', 'hls_file_480', 'hls_file_720', 'hls_file_1080']


    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['title', 'video_file', 'hls_file_360', 'hls_file_480', 'hls_file_720', 'hls_file_1080']
        else:
            return []
