import os
from metadata_extractor import get_image_metadata
from unique_filename_generator import generate_unique_suffix

def rename_files(folder_path, output_path):
    print('works file_renamer')

    file_counts = {}  # Dictionary to store file counts for serial numbers
    for root, _, filenames in os.walk(folder_path):
        for filename in filenames:
            if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
                image_path = os.path.join(root, filename)
                lat, lon, photo_datetime, image_url = get_image_metadata(image_path)
                
                if lat is not None and lon is not None and photo_datetime is not None:
                    lat_str = str(int(lat * 10000)).replace('.', '')
                    lon_str = str(int(lon * 10000)).replace('.', '')
                    date_str = photo_datetime.strftime("%Y-%m")
                    new_filename_base = f"{lat_str}.{lon_str}.{date_str}"

                    if new_filename_base in file_counts:
                        file_counts[new_filename_base] += 1
                    else:
                        file_counts[new_filename_base] = 1

                    # serial_number = str(file_counts[new_filename_base]).zfill(5)
                    unique_suffix = generate_unique_suffix()
                    new_filename = f"{new_filename_base}.{unique_suffix}.jpg"
                    new_image_path = os.path.join(output_path, new_filename)
                    # Rename the file
                    os.rename(image_path, new_image_path)
                    print(f"Renamed {filename} to {new_filename}")
                else:
                    print(f"Metadata missing for {filename}, skipping.")
    