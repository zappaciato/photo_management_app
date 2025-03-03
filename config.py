# config.py
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Project's root directory

OTHER_TYPE_FILES_PATH = os.path.join(BASE_DIR, "RESULT", "other_type_files")
UTILITY_BASE_FOLDER_PATH = os.path.join(BASE_DIR, "Photos")
OUTPUT_PATH = os.path.join(BASE_DIR, "RESULT")
UPDATED_PHOTOS_PATH = os.path.join(BASE_DIR, "RESULT", "updated_files")
THUMBS_PATH = os.path.join(BASE_DIR, "RESULT", "Thumbs")
EDITED_FILES_PATH = os.path.join(BASE_DIR, "Result", "edited_files")
VIDEO_FILES_PATH = os.path.join(BASE_DIR, "Result", "video_files")
EDITED_VIDEOS_PATH = os.path.join(BASE_DIR, "Result", "edited_videos")
VIDEO_THUMBS_PATH = os.path.join(BASE_DIR, "Result", "video_thumbs")

AUDIO_FILES_PATH = os.path.join(BASE_DIR, "Result", "audio_files")