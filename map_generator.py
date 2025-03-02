import folium
import os
from metadata_extractor import get_image_metadata
from thumbnails_generator import create_thumbnail_file, create_thumbnail_folder


def create_photo_map(output_path):

    """Creates an HTML map with markers for photos with GPS data.  Creates an HTML map with separate thumbnail files and links to original images."""
    m = folium.Map(location=[0, 0], zoom_start=2)
    image_dir = create_thumbnail_folder(output_path)

    for root, _, filenames in os.walk(output_path):
        # if root not in initial_folders:
        #     continue
        for filename in filenames:
            if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
                image_path = os.path.join(root, filename)
                metadata = get_image_metadata(image_path)
                print("Colected metadata")

                            # Calculate relative path
                            # relative_path = os.path.relpath(image_path)
                relative_path = os.path.relpath(image_path, output_path).replace(os.sep, '/')
                print("________________FOR_FILE::__________________")
                print(relative_path)
                if metadata:
                    print("About to create Thumbnail file......")
                thumb_filename = create_thumbnail_file(image_dir, filename, image_path)
                                # lat, lon, photo_datetime, data_url = metadata
                lat, lon, photo_datetime = metadata
                popup_text = f"<b>{filename}</b>"
                if photo_datetime:
                    popup_text += f"<br>Date/Time: {photo_datetime}"

                popup_text += f"<br><a href='{relative_path}' target='_blank'><img src='thumbnails/{thumb_filename}' width='100'></a>"

                print("About to generate a map")
                folium.Marker(location=[lat, lon], popup=popup_text).add_to(m)

                m.save(os.path.join(output_path, 'photo_map.html'))