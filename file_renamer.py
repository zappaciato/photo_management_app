import os
from metadata_extractor import get_image_metadata, format_metadata
from unique_filename_generator import generate_unique_suffix

def rename(new_filename_base, unique_suffix, output_path, image_path, filename):
    new_filename = f"{new_filename_base}.{unique_suffix}.jpg"
    new_image_path = os.path.join(output_path, new_filename)
    # Rename the file
    os.rename(image_path, new_image_path)
    print(f"Renamed {filename} to {new_filename}")

def rename_files(folder_path, output_path):
    for root, _, filenames in os.walk(folder_path):
        for filename in filenames:
            if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
                image_path = os.path.join(root, filename)
                lat, lon, photo_datetime = get_image_metadata(image_path)
                
                if lat is not None and lon is not None and photo_datetime is not None:
                    print("about to cread new filename base")

                    new_filename_base = format_metadata(lat, lon, photo_datetime)
                    unique_suffix = generate_unique_suffix()
                    rename(new_filename_base, unique_suffix, output_path, image_path, filename)

                else:       
                    print(f"Metadata missing for {filename}, skipping.")
                    # lat, lon, photo_datetime = get_image_metadata(image_path)
    