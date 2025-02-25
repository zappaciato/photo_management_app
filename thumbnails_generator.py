from PIL import Image

def create_thumbnail(image_path, thumb_path, size=(400, 300)):
    """Creates a thumbnail image file."""

    try:
        img = Image.open(image_path)
        img.thumbnail(size)
        img.save(thumb_path)
        print("successfully creating thumbs")

    except Exception as e:
        print(f"Error creating thumbnail: {e}")