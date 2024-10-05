import os
import sys
import django

sys.path.append('/home/zuegelwagen/videoflix-backend')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'videoflix_backend.settings')
django.setup()

from content.admin import VideoResource

dataset = VideoResource().export()

with open('backup_data.json', 'w') as f:
    f.write(dataset.json)

print("Data exported to backup_data.json")
