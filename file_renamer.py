import os
from metadata_extractor import get_image_metadata, format_metadata
from unique_filename_generator import generate_unique_suffix
import shutil
from file_validation import validate_file

# def rename(new_filename_base, unique_suffix, image_path, filename, output_path):
#     new_filename = f"{new_filename_base}.{unique_suffix}.jpg"
#     # new_image_path = os.path.join(output_path, new_filename)
#     new_image_path = os.path.join(os.path.dirname(image_path), new_filename)
#     # new_image_path = os.path.join(output_path, new_filename)  # Use output_path here
#     # Rename the file
#     os.rename(image_path, new_image_path)
#     print(f"Renamed {filename} to {new_filename}")

def rename_files(folder_path, output_path):

    edited_folder = os.path.join(output_path, "edited_files")  # Create edited_folder path in the root folder
    video_folder = os.path.join(output_path, "video_files")
    result_folder = os.path.join(output_path, "updated_files")
    print('Here is edited and video folder path')
    print(edited_folder)
    print(video_folder)
    print(result_folder)

    for root, _, filenames in os.walk(folder_path):
            # if root not in initial_folders:
                # continue

            for filename in filenames:
                image_path = os.path.join(root, filename)
                file_status = validate_file(image_path)

                if file_status == "video":
                    print("Found a video file")
                    os.makedirs(video_folder, exist_ok=True)
                    shutil.move(image_path, os.path.join(video_folder, filename))
                    print(f"Moved {filename} to video_files folder.")

                elif isinstance(file_status, tuple) and len(file_status) == 3: # Check if it is a tuple of 3 items.:
                    print("found a valid photo file and processing name...")
                    lat, lon, photo_datetime = file_status
                    new_filename_base = format_metadata(lat, lon, photo_datetime)
                    unique_suffix = generate_unique_suffix()
                    new_filename = f"{new_filename_base}.{unique_suffix}.jpg"

                    new_image_path = os.path.join(os.path.dirname(image_path), new_filename)
                    os.rename(image_path, new_image_path)
                    print(f"Renamed {filename} to {new_filename}")

                    os.makedirs(result_folder, exist_ok=True)
                    # shutil.copy(new_image_path, os.path.join(result_folder, new_filename))
                    shutil.move(new_image_path, os.path.join(result_folder, new_filename))
                    print(f"Moved {filename} to {result_folder} folder.")

                elif file_status == False:
                    print("Found foto file with metadata missing or edited...")
                    os.makedirs(edited_folder, exist_ok=True)
                    shutil.move(image_path, os.path.join(edited_folder, filename))
                    print(f"Moved {filename} to edited_files folder.")
                else:
                    print(f"File {filename} is not a video or photo and was not processed.")



