from PIL import Image
import os

def create_thumbnail_folder(output_path):
    image_dir = os.path.join(output_path, "thumbnails")  # Create a thumbnails directory
    os.makedirs(image_dir, exist_ok=True)
    return image_dir

def create_thumbnail_file(image_dir, filename, image_path):
    """Creates a thumbnail file and returns its path."""
    try:
        thumb_filename = f"{os.path.splitext(filename)[0]}.thumb.jpg"
        thumb_path = os.path.join(image_dir, thumb_filename)
        create_thumbnail(image_path, thumb_path)
        return thumb_filename
    except Exception as e:
        print(f"Error creating thumbnail for {filename}: {e}")
        return None  # Return None if thumbnail creation fails

def create_thumbnail(image_path, thumb_path, size=(400, 300)):
    """Creates a thumbnail image file."""
    # print(f"Thumbnail image_path: {image_path}") #Debug print
    # print(f"Thumbnail thumb_path: {thumb_path}") #Debug print
    try:
        img = Image.open(image_path)
        img.thumbnail(size)
        img.save(thumb_path)
        print("successfully creating thumbs")

    except Exception as e:
        print(f"Error creating thumbnail: {e}")