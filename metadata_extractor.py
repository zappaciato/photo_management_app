import exifread
from utils import gps_to_decimal, parse_datetime
# from thumbnails_generator import create_thumbnail

def get_image_metadata(image_path):
    """Extracts GPS coordinates, direction, and datetime from an image."""

    try:
        with open(image_path, 'rb') as f:
            tags = exifread.process_file(f)

            if 'GPS GPSLatitude' in tags and 'GPS GPSLongitude' in tags:
                lat = gps_to_decimal(tags['GPS GPSLatitude'].values)
                lon = gps_to_decimal(tags['GPS GPSLongitude'].values)
                photo_datetime = parse_datetime(tags.get('Image DateTime'))
                return lat, lon, photo_datetime
            # if tags is None : #tutaj jest cos nie tak
            #     lat = 00
            #     lon = 00
            #     photo_datetime = "xxxx-xx"
            #     return lat, lon, photo_datetime
    except (FileNotFoundError, KeyError, ValueError, exifread.heic.NoParser) as e:
        print(f"Error processing {image_path}: {e}")
        return lat, lon, photo_datetime
        
def format_metadata(lat, lon, photo_datetime):
    lat_str = str(int(lat * 10000)).replace('.', '')
    lon_str = str(int(lon * 10000)).replace('.', '')
    date_str = photo_datetime.strftime("%Y-%m")

    return f"{lat_str}.{lon_str}.{date_str}"