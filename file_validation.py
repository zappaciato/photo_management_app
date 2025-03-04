import os
from metadata_extractor import get_image_metadata  # Assuming you have this module

def validate_file(image_path):

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
            # ponizej na wypadekmjesli w meta danych znajdzie sie chociaz data. 
            # elif lat is None and lon is None and photo_datetime is not None:
            #     lat == 00000 , lon == 00000
            #     return lat, lon, photo_datetime

            else:
                return False

        except Exception: #Catch any errors from the metadata reading.
            return False # If there is an error, we can assume metadata missing.

    elif filename.lower().endswith(('.txt', '.doc', '.docx', '.xls', '.xlsx', '.pdf')):
        return "other_file_type"
    
    elif filename.lower().endswith(('.mp3', '.wav', '.flac', '.aac', '.ogg')): #added audio
        return "audio_file"