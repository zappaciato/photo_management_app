import folium
import os
from metadata_extractor import get_image_metadata
from thumbnails_generator import create_thumbnail

def create_photo_map(folder_path, output_path):
    """Creates an HTML map with markers for photos with GPS data."""
    m = folium.Map(location=[0, 0], zoom_start=2)

    image_dir = os.path.join(output_path, "thumbnails")  # Create a thumbnails directory
    os.makedirs(image_dir, exist_ok=True)

    print('works create phot map')

    for root, _, filenames in os.walk(folder_path):
        for filename in filenames:
            if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
                image_path = os.path.join(root, filename)
                metadata = get_image_metadata(image_path)
                
                # Create thumbnail file
                thumb_filename = f"{os.path.splitext(filename)[0]}.thumb.jpg"
                thumb_path = os.path.join(image_dir, thumb_filename)
                create_thumbnail(image_path, thumb_path)


                print("cerated thumbnail")
                if metadata:
                    # lat, lon, photo_datetime, data_url = metadata
                    lat, lon, photo_datetime = metadata
                    popup_text = f"<b>{filename}</b>"
                    if photo_datetime:
                        popup_text += f"<br>Date/Time: {photo_datetime}"
                    # popup_text += f"<br><img src='{image_dir}' width='100'>"

                    popup_text += f"<br><a href='{filename}' target='_blank'><img src='thumbnails/{thumb_filename}' width='100'></a>"
                    # folium.Marker(location=[lat, lon], popup=popup_text).add_to(m)


                    print("About to generate a map")
                    folium.Marker(location=[lat, lon], popup=popup_text).add_to(m)

    m.save(os.path.join(output_path, 'photo_map.html'))