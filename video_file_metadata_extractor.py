import subprocess
import json
import os
from datetime import datetime
from PIL import Image

def get_video_metadata(video_path):
    """Extracts video metadata using ffprobe."""
    try:
        command = [
            'ffprobe',
            '-v', 'quiet',
            '-print_format', 'json',
            '-show_format',
            '-show_streams',
            video_path,
        ]
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        metadata = json.loads(result.stdout)

        duration = float(metadata['format']['duration']) if 'format' in metadata and 'duration' in metadata['format'] else None
        creation_time = metadata['format']['tags']['creation_time'] if 'format' in metadata and 'tags' in metadata['format'] and 'creation_time' in metadata['format']['tags'] else None

        # Attempt to extract lat/lon (often not present in video metadata)
        lat = None
        lon = None
        if 'streams' in metadata:
            for stream in metadata['streams']:
                if 'tags' in stream:
                    if 'location' in stream['tags']:
                        location = stream['tags']['location']
                        try:
                            lat, lon = map(float, location.split('+')[1:])
                        except ValueError:
                            pass #location tag exists, but is malformed.

        return {
            'duration': duration,
            'creation_time': creation_time,
            'lat': lat,
            'lon': lon,
        }
    except (subprocess.CalledProcessError, FileNotFoundError, json.JSONDecodeError, KeyError) as e:
        print(f"Error extracting metadata from {video_path}: {e}")
        return None

def generate_video_thumbnail(video_path, output_path, thumb_filename):
    """Generates a thumbnail from the first frame of a video."""
    try:
        (
            ffmpeg
            .input(video_path)
            .filter('scale', 200, -1)  # Resize thumbnail
            .output(os.path.join(output_path, thumb_filename), vframes=1)
            .run(quiet=True, overwrite_output=True)
        )
        return True
    except ffmpeg.Error as e:
        print(f"Error creating thumbnail from {video_path}: {e.stderr}")
        return False