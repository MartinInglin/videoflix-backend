import subprocess
import os

def convert(source):
    file_name_no_suffix = create_file_name_no_suffix(source)
    convert_video(source, file_name_no_suffix, '640x360', '_360p.mp4')
    convert_video(source, file_name_no_suffix, '854x480', '_480p.mp4')
    convert_video(source, file_name_no_suffix, '1280x720', '_720p.mp4')
    convert_video(source, file_name_no_suffix, '1920x1080', '_1080p.mp4')

def convert_video(source, file_name_no_suffix, resolution, resolution_suffix):
    new_file_name = file_name_no_suffix + resolution_suffix
    cmd = '{ffmpeg} -i "{source}" -s {resolution} -c:v libx264 -crf 23 -c:a aac -strict -2 "{file_name}"'.format(
        ffmpeg="/usr/bin/ffmpeg",
        source=source,
        resolution=resolution,
        file_name=new_file_name
        )
    run = subprocess.run(cmd, capture_output=True, text=True, shell=True)

def delete_videos(file_path):
    file_name_no_suffix = create_file_name_no_suffix(file_path)
    delete_video(file_path, '')
    delete_video(file_name_no_suffix, '_360p.mp4')
    delete_video(file_name_no_suffix, '_480p.mp4')
    delete_video(file_name_no_suffix, '_720p.mp4')
    delete_video(file_name_no_suffix, '_1080p.mp4')

def delete_video(file_path, resolution_suffix):
    file_path = file_path + resolution_suffix
    if os.path.isfile(file_path):
        os.remove(file_path)

def create_file_name_no_suffix(source):
    return os.path.splitext(source)[0]
