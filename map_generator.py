import os
import folium
from metadata_extractor import get_image_metadata
from thumbnails_generator import create_thumbnail_folder, create_thumbnail_file

def create_photo_map(images_path, thumbs_path):
    """Creates an HTML map with markers for photos, grouping photos with the same location into a single marker's popup."""
    m = folium.Map(location=[0, 0], zoom_start=2)
    image_dir = create_thumbnail_folder(thumbs_path)
    location_photos = {}  # Dictionary to store photos by location

    for root, _, filenames in os.walk(images_path):
        for filename in filenames:
            if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
                image_path = os.path.join(root, filename)
                metadata = get_image_metadata(image_path)
                print("Collected metadata")

                relative_image_path = os.path.relpath(image_path, thumbs_path).replace(os.sep, '/')
                relative_path = os.path.relpath(image_path, images_path).replace(os.sep, '/')
                print("________________FOR_FILE::__________________")
                print(relative_path)
                if metadata:
                    print("About to create Thumbnail file......")
                    thumb_filename = create_thumbnail_file(image_dir, filename, image_path)
                    lat, lon, photo_datetime = metadata
                    location = (lat, lon)  # Create location tuple

                    photo_info = {
                        'filename': filename,
                        'relative_image_path': relative_image_path,
                        'thumb_filename': thumb_filename,
                        'photo_datetime': photo_datetime
                    }

                    if location in location_photos:
                        location_photos[location].append(photo_info)
                    else:
                        location_photos[location] = [photo_info]

    # Create markers from grouped photos
    for location, photos in location_photos.items():
        lat, lon = location
        popup_text = "<div style='max-height: 500px; overflow-y: auto;'>"
        for photo in photos:
            popup_text += f"<b>{photo['filename']}</b>"
            if photo['photo_datetime']:
                popup_text += f"<br>:: {photo['photo_datetime']} ::"
            popup_text += f"<br><a href='{photo['relative_image_path']}' target='_blank'><img src='thumbnails/{photo['thumb_filename']}' width='600' height='400'></a><br>"

        print("Putting the photo on a map.....")
        folium.Marker(location=[lat, lon], popup=popup_text).add_to(m)

    m.save(os.path.join(thumbs_path, 'photo_map.html'))