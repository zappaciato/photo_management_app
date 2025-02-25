import os
import exifread
import folium
from PIL import Image
import base64
from datetime import datetime

def get_gps_coordinates_and_direction(image_path):

    try:
        with open(image_path, 'rb') as f:
            tags = exifread.process_file(f)
            print(tags['Image DateTime'])
            print("ciecjhuj")
            if 'GPS GPSLatitude' in tags and 'GPS GPSLongitude' in tags:
                lat = gps_to_decimal(tags['GPS GPSLatitude'].values)
                lon = gps_to_decimal(tags['GPS GPSLongitude'].values)

                if 'GPS ImgDirection' in tags:
                    direction = float(tags['GPS ImgDirection'].values) 
                    print(direction)
                else:
                    direction = None 
                    print('no directions')
                
                if 'Image DateTime' in tags:
                    # print(tags['Image DateTime'])
                    print('chuj')
                    try:
                        datetime_str = str(tags['Image DateTime'])
                        
                        photo_datetime = datetime.strptime(datetime_str, "%Y:%m:%d %H:%M:%S") 
                        
                    except (ValueError, TypeError):
                        photo_datetime = None
                        print("jakis error date and time") 
                else:
                    photo_datetime = None
                    print('no date and time')

                return lat, lon, direction, photo_datetime
            
    except (FileNotFoundError, KeyError, ValueError, exifread.heic.NoParser) as e:
        print(f"Error processing {image_path}: {e}")
        return None

def gps_to_decimal(coords):
    """Converts GPS coordinates from Exif format to decimal degrees."""
    degrees = coords[0]
    minutes = coords[1] / 60.0
    seconds = coords[2] / 3600.0
    return degrees + minutes + seconds

def create_photo_map(folder_path, output_path):
    """
    Creates an HTML map with markers for photos with GPS data.

    Args:
        folder_path: Path to the folder containing photos.
        output_path: Path to the desired output directory for the HTML file.
    """
    m = folium.Map(location=[0, 0], zoom_start=2) 
    for root, _, filenames in os.walk(folder_path):
        print(filenames)
        for filename in filenames:
            if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
                image_path = os.path.join(root, filename)
                coords_and_direction = get_gps_coordinates_and_direction(image_path)
                if coords_and_direction:
                    lat, lon, direction, photo_datetime = coords_and_direction
                    popup_text = f"<b>{filename}</b><br>Direction: {direction:.2f} degrees" if direction else filename
                    if direction:
                        popup_text += f"<br>Direction: {direction:.2f} degrees"
                    if photo_datetime:
                        popup_text += f"<br>Date/Time: {photo_datetime}" 
                    # Create a thumbnail 
                    with open(image_path, "rb") as image_file:
                        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
                    data_url = f"data:image/jpeg;base64,{encoded_string}"  # Adjust image/jpeg if needed
                    popup_text += f"<br><img src='{data_url}' width='100'>" 
                    folium.Marker(location=[lat, lon], popup=popup_text).add_to(m)

    m.save(os.path.join(output_path, 'photo_map.html'))

if __name__ == "__main__":
    folder_path = r"C:\Users\kflakiewicz\Desktop\Media_Kris\GeoPhoto_app\Photos" 
    output_directory = r"C:\Users\kflakiewicz\Desktop\Media_Kris\GeoPhoto_app\Photos"  
    create_photo_map(folder_path, output_directory)