import os
import folium
from metadata_extractor import get_image_metadata
from thumbnails_generator import create_thumbnail_folder, create_thumbnail_file
import json
from datetime import datetime

def create_photo_map(images_path, thumbs_path, output_dir='Result', output_file='thumbnail_map.html'):
    """Creates an HTML map with a thumbnail sidebar and larger thumbnail with details on marker click."""
    print(f"Images path: {images_path}")
    print(f"Thumbs path: {thumbs_path}")

    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, output_file)

    m = folium.Map(location=[0, 0], zoom_start=2)
    image_dir = create_thumbnail_folder(thumbs_path)
    photo_data = []

    for root, _, filenames in os.walk(images_path):
        for filename in filenames:
            if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
                image_path = os.path.join(root, filename)
                print(f"Processing image: {image_path}")
                metadata = get_image_metadata(image_path)
                print(f"Metadata: {metadata}")
                if metadata:
                    thumb_filename = create_thumbnail_file(image_dir, filename, image_path)
                    print(f"Thumbnail created: {thumb_filename}")
                    lat, lon, photo_datetime = metadata
                    relative_image_path = os.path.relpath(image_path, thumbs_path).replace(os.sep, '/')
                    thumb_relative_path = os.path.join('thumbnails', thumb_filename).replace(os.sep, '/')

                    if photo_datetime:
                        try:
                            photo_datetime_str = photo_datetime.strftime('%Y-%m-%d %H:%M:%S')
                        except AttributeError:
                            photo_datetime_str = photo_datetime
                    else:
                        photo_datetime_str = None

                    photo_data.append({
                        'lat': lat,
                        'lon': lon,
                        'thumb_filename': thumb_relative_path,
                        'relative_image_path': relative_image_path,
                        'filename': filename,
                        'photo_datetime': photo_datetime_str
                    })
                    print(f"Photo data appended: {photo_data[-1]}")
                else:
                    print(f"No metadata for: {image_path}")
    print(f"Total photos with data: {len(photo_data)}")

    js_data = json.dumps(photo_data)
    sidebar_html = '<div id="sidebar" style="width: 50%;  height: 100vh; overflow-y: auto; float: right;">'
    for photo in photo_data:
        sidebar_html += f'<div style="text-align: center; font-size: 10px; ">{photo["filename"]}</div><img src="{photo["thumb_filename"]}" width="95%" style="border: 1px solid #ccc; margin: 1% 2% 0 2%; cursor: pointer;" onclick="showLocation({photo["lat"]}, {photo["lon"]}, \'{photo["thumb_filename"]}\', \'{photo["relative_image_path"]}\', \'{photo["filename"]}\', \'{photo["photo_datetime"]}\');" title="{photo["filename"]}"/><br>'
    sidebar_html += '</div>'

    js_code = f"""
    <script>
        var photoData = {js_data};
        var currentMarker = null;
        var fixedPopupWidth = 800;
        var fixedPopupHeight = 250;

        function showLocation(lat, lon, thumbPath, imagePath, filename, photoDatetime) {{
            map.setView([lat, lon], 12);
            if (currentMarker) {{
                map.removeLayer(currentMarker);
            }}
            var popupContent = '<div ><b>' + filename + '</b><br>';
            if (photoDatetime) {{
                popupContent += ':: ' + photoDatetime + ' ::<br>';
            }}
            popupContent += '<a href="' + imagePath + '" target="_blank"><img src="' + thumbPath + '" style="max-width: 100%; max-height: 80%;"></a></div>';
            currentMarker = L.marker([lat, lon]).addTo(map).bindPopup(popupContent);
            currentMarker.openPopup();
        }}
    </script>
    """

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Thumbnail Map</title>
        <meta charset="utf-8" />
        <meta name="viewport" content="width:device-width, initial-scale=1.0">
        <link rel="stylesheet" href="https://unpkg.com/leaflet@1.7.1/dist/leaflet.css" />
        <script src="https://unpkg.com/leaflet@1.7.1/dist/leaflet.js"></script>
        <style>
            #map {{ position: absolute; top: 0; left: 0; width: 50%; height: 100vh; }}
        </style>
    </head>
    <body>
        <div id="map"></div>
        {sidebar_html}
        {js_code}
        <script>
            var map = L.map('map').setView([0, 0], 2);
            L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png').addTo(map);
        </script>
    </body>
    </html>
    """

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)