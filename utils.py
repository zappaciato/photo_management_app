from datetime import datetime

def gps_to_decimal(coords):
    """Converts GPS coordinates from Exif format to decimal degrees."""
    degrees = coords[0]
    minutes = coords[1] / 60.0
    seconds = coords[2] / 3600.0
    return degrees + minutes + seconds

def parse_datetime(datetime_str):
    """Parses a datetime string."""
    try:
        return datetime.strptime(str(datetime_str), "%Y:%m:%d %H:%M:%S")
    except (ValueError, TypeError):
        return None
    
    