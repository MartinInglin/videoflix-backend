## System Requirements

- Python 3.x
- Redis
- FFmpeg (for media processing)

To install FFmpeg on Ubuntu:

```bash
sudo apt install ffmpeg
```

## Video Upload Limitations

Currently, the application only supports video uploads from Linux-based systems. This limitation is due to differences in file system paths and permissions when uploading videos from non-Linux operating systems (such as Windows or macOS).

Known Issue:

    Uploads from Windows or macOS systems: Attempting to upload videos from these operating systems may result in file path issues or permission errors. For now, ensure that video files are uploaded from a Linux environment.

Future Improvements:

    Support for video uploads from Windows and macOS is under consideration for future development.