import os
from metadata_extractor import get_image_metadata  # Assuming you have this module

def validate_file(image_path):
    """
    Validates a file and returns a status code indicating its type or issues.

    Returns:
        "video": If the file is a video.
        "metadata_missing": If the file is an image but lacks metadata.
        "other": If the file is neither a video nor a valid image with metadata.
        "valid_image": If the file is an image with all necessary metadata.
    """
    filename = os.path.basename(image_path)  # Extract filename for checks

    if filename.lower().endswith(('.mp4', '.avi', '.mov')):
        return "video"

    elif filename.lower().endswith(('.jpg', '.jpeg', '.png')):
        try:
            lat, lon, photo_datetime = get_image_metadata(image_path)
            print("here are the metadata details:>>>>>>>>>>>>>>>>")
            print(lat)
            print(lon)
            print(photo_datetime)
            print("End of details lat lon date>>>>>>>>>>>>>>>>>")
            if lat is not None and lon is not None and photo_datetime is not None:
                return lat, lon, photo_datetime
            elif lat is None and lon is None and photo_datetime is not None:
                lat == 00000 , lon == 00000
                return lat, lon, photo_datetime

            else:
                return False

        except Exception: #Catch any errors from the metadata reading.
            return False # If there is an error, we can assume metadata missing.

    else:
        return "other"