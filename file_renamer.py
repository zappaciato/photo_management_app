import os
import config
from metadata_extractor import get_image_metadata, format_metadata
from unique_filename_generator import generate_unique_suffix
import shutil
from file_validation import validate_file
from report_generator import generate_report_html



def rename_files(folder_path, output_path):

    edited_folder = config.EDITED_FILES_PATH
    edited_files_count = 0
    video_folder = config.VIDEO_FILES_PATH
    video_files_count = 0
    audio_folder = config.AUDIO_FILES_PATH
    audio_files_count = 0
    result_folder = config.UPDATED_PHOTOS_PATH
    updated_files_count = 0
    other_files = config.OTHER_TYPE_FILES_PATH
    other_files_count = 0

    for root, _, filenames in os.walk(folder_path):
        for filename in filenames:
            image_path = os.path.join(root, filename)
            #validate what file we are scanning
            file_status = validate_file(image_path)
            #depending on the status take action
            if file_status == "video":
                print("Found a video file")
                os.makedirs(video_folder, exist_ok=True)
                shutil.move(image_path, os.path.join(video_folder, filename))
                print(f"Moved {filename} to video_files folder.")
                video_files_count += 1

            elif isinstance(file_status, tuple) and len(file_status) == 3: # Check if it is a tuple of 3 items.:

                print("Found a valid photo file and processing its name...")
                lat, lon, photo_datetime = file_status
                new_filename_base = format_metadata(lat, lon, photo_datetime)
                unique_suffix = generate_unique_suffix()
                new_filename = f"{new_filename_base}.{unique_suffix}.jpg"
                    
                print("New name created and about to rename the file...")
                new_image_path = os.path.join(os.path.dirname(image_path), new_filename)
                os.rename(image_path, new_image_path)
                print(f"Renamed {filename} to {new_filename}")

                os.makedirs(result_folder, exist_ok=True)
                # shutil.copy(new_image_path, os.path.join(result_folder, new_filename))
                shutil.move(new_image_path, os.path.join(result_folder, new_filename))
                print(f"Moved {filename} to {result_folder} folder.")

                updated_files_count += 1

            elif file_status == False:
                print("Found foto file with metadata missing due to editing...")
                os.makedirs(edited_folder, exist_ok=True)
                shutil.move(image_path, os.path.join(edited_folder, filename))
                print(f"Moved {filename} to edited_files folder.")

                edited_files_count += 1
                
            elif file_status == "other_file_type":
                print("Found other type of file: .doc, .xls or PDF")
                os.makedirs(other_files, exist_ok=True)
                shutil.move(image_path, os.path.join(other_files, filename))
                print(f"Moved {filename} to other_files folder.")

                other_files_count += 1
                
            elif file_status == "audio_file":
                print("Found audio file")
                os.makedirs(audio_folder, exist_ok=True)
                shutil.move(image_path, os.path.join(audio_folder, filename))
                print(f"Moved {filename} to other_files folder.")

                audio_files_count += 1

            else:
                print(f"File {filename} is not a video or photo or a document and was not processed. Check your original folder!")

    generate_report_html(audio_files_count, other_files_count, video_files_count, updated_files_count, edited_files_count)


