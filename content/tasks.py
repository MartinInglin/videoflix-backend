import subprocess
import os
import shutil
from django.db import transaction
from content.models import Video

def convert(source, folder_path):

    base_name = os.path.splitext(os.path.basename(source))[0]
    output_dir = os.path.join('media', 'videos', folder_path, 'HLS_files')
    os.makedirs(output_dir, exist_ok=True)

    resolutions = {
        '360p': ('hls_file_360', '640x360'),
        '480p': ('hls_file_480', '854x480'),
        '720p': ('hls_file_720', '1280x720'),
        '1080p': ('hls_file_1080', '1920x1080')
    }

    with transaction.atomic():
        video_instance = Video.objects.get(title=folder_path)
    
        for suffix, (field_name, resolution) in resolutions.items():
            resolution_file = os.path.join(output_dir, f"{base_name}_{suffix}.mp4")
            convert_to_resolution(source, resolution_file, resolution)
            
            hls_prefix = os.path.join(output_dir, f"{base_name}_{suffix}")
            m3u8_path = convert_to_hls(resolution_file, hls_prefix)

            setattr(video_instance, field_name, m3u8_path.replace('media/', ''))

            delete_mp4(resolution_file)

        video_instance.save()

def convert_to_resolution(source, output_name, resolution):
    cmd = [
        "/usr/bin/ffmpeg", "-i", source,
        "-s", resolution, "-c:v", "libx264", "-crf", "23", "-c:a", "aac", "-strict", "-2",
        output_name
    ]
    subprocess.run(cmd, check=True)

def convert_to_hls(source, output_name_prefix):
    m3u8_file = f"{output_name_prefix}.m3u8"
    segment_pattern = f"{output_name_prefix}_%03d.ts"
    cmd = [
        "/usr/bin/ffmpeg", "-i", source, "-codec", "copy", "-start_number", "0",
        "-hls_time", "10", "-hls_list_size", "0", "-f", "hls",
        "-hls_segment_filename", segment_pattern, m3u8_file
    ]
    subprocess.run(cmd, check=True)
    return m3u8_file

def save_hls_path_to_video_instance(title, m3u8_path):
    video_instance = Video.objects.get(title=title)
    video_instance.hls_playlist = m3u8_path.replace('media/', '')
    video_instance.save()

def delete_mp4(resolution_file):
    if os.path.exists(resolution_file):
        os.remove(resolution_file)

def delete_video_folder(folder_path):
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)

