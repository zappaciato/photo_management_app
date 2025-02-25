import folium
import os
from metadata_extractor import get_image_metadata

def create_photo_map(folder_path, output_path):
    """Creates an HTML map with markers for photos with GPS data."""
    m = folium.Map(location=[0, 0], zoom_start=2)
    print('works create phot map')
    for root, _, filenames in os.walk(folder_path):
        for filename in filenames:
            if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
                image_path = os.path.join(root, filename)
                metadata = get_image_metadata(image_path)

                if metadata:
                    lat, lon, photo_datetime, data_url = metadata
                    popup_text = f"<b>{filename}</b>"
                    if photo_datetime:
                        popup_text += f"<br>Date/Time: {photo_datetime}"
                    popup_text += f"<br><img src='{data_url}' width='100'>"
                    folium.Marker(location=[lat, lon], popup=popup_text).add_to(m)

    m.save(os.path.join(output_path, 'photo_map.html'))