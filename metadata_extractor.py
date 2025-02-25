import exifread
from utils import gps_to_decimal, parse_datetime
from thumbnails_generator import create_thumbnail

def get_image_metadata(image_path):
    """Extracts GPS coordinates, direction, and datetime from an image."""

    try:
        with open(image_path, 'rb') as f:
            tags = exifread.process_file(f)

            if 'GPS GPSLatitude' in tags and 'GPS GPSLongitude' in tags:
                lat = gps_to_decimal(tags['GPS GPSLatitude'].values)
                lon = gps_to_decimal(tags['GPS GPSLongitude'].values)

                photo_datetime = parse_datetime(tags.get('Image DateTime'))

                # # Create a thumbnail base64
                # with open(image_path, "rb") as image_file:
                #     encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
                # data_url = f"data:image/jpeg;base64,{encoded_string}"

                # thumbnail_path = create_thumbnail(image_path)

                # return lat, lon, photo_datetime, data_url
                return lat, lon, photo_datetime
            else:
                return None
    except (FileNotFoundError, KeyError, ValueError, exifread.heic.NoParser) as e:
        print(f"Error processing {image_path}: {e}")
        return None