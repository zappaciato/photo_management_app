import os
from metadata_extractor import get_image_metadata, format_metadata
from unique_filename_generator import generate_unique_suffix
import shutil

def rename(new_filename_base, unique_suffix, image_path, filename, output_path):
    new_filename = f"{new_filename_base}.{unique_suffix}.jpg"
    # new_image_path = os.path.join(output_path, new_filename)
    new_image_path = os.path.join(os.path.dirname(image_path), new_filename)
    # new_image_path = os.path.join(output_path, new_filename)  # Use output_path here
    # Rename the file
    os.rename(image_path, new_image_path)
    print(f"Renamed {filename} to {new_filename}")

def rename_files(folder_path, output_path):

    edited_folder = os.path.join(output_path, "edited_files")  # Create edited_folder path in the root folder
    video_folder = os.path.join(output_path, "video_files")
    result_folder = os.path.join(output_path, "updated_files")
    print('Here is edited and video folder path')
    print(edited_folder)
    print(video_folder)
    print(result_folder)
    #to prevent scanning newly created folders by application
    # initial_folders = [
    #     os.path.join(folder_path, name)
    #     for name in os.listdir(folder_path)
    #     if os.path.isdir(os.path.join(folder_path, name))
    # ]
    
    # for initial_folder in initial_folders:
    for root, _, filenames in os.walk(folder_path):
            # if root not in initial_folders:
                # continue

            for filename in filenames:
                image_path = os.path.join(root, filename)
                if filename.lower().endswith(('.mp4', '.avi', '.mov')):
                    os.makedirs(video_folder, exist_ok=True)
                    shutil.move(image_path, os.path.join(video_folder, filename))
                    print(f"Moved {filename} to video_files folder.")

                elif filename.lower().endswith(('.jpg', '.jpeg', '.png')):
                    # Initialize variables before the try block
                    lat = None
                    lon = None
                    photo_datetime = None
                    try:
                        lat, lon, photo_datetime = get_image_metadata(image_path)
                    except Exception as e:
                        print(f"Fucked up {filename}: {e}")

                    if lat is not None and lon is not None and photo_datetime is not None:
                        print("about to cread new filename base - details form metadata - for renaming")

                        new_filename_base = format_metadata(lat, lon, photo_datetime)
                        unique_suffix = generate_unique_suffix()
                        new_filename = f"{new_filename_base}.{unique_suffix}.jpg"

                        new_image_path = os.path.join(os.path.dirname(image_path), new_filename)
                        os.rename(image_path, new_image_path)
                        print(f"Renamed {filename} to {new_filename}")
                        # shutil.move(image_path, os.path.join(result_folder, filename))
                        # rename(new_filename_base, unique_suffix, image_path, filename, output_path)
                        # new_image_path = rename(new_filename_base, unique_suffix, image_path, filename, output_path)
                        # print(f"Moved {os.path.basename(new_image_path)} to {output_path}")
                        # os.makedirs(result_folder, exist_ok=True)

                    else:
                        os.makedirs(edited_folder, exist_ok=True) 
                        # copy files there only if there any to be copied. 
                        shutil.move(image_path, os.path.join(edited_folder, filename))
                        print(f"Moved {filename} to edited_files folder.")
                        # edited_folder = os.path.join(os.path.dirname(image_path), "edited_files")
                        # os.makedirs(edited_folder, exist_ok=True)
                        # shutil.move(image_path, os.path.join(edited_folder, filename))
                        # print(f"Moved {filename} to edited_files folder.")
                        
                        # new_filename_base = "edited_file"
                        # unique_suffix = generate_unique_suffix()
                        # rename(new_filename_base, unique_suffix, output_path, image_path, filename)       
                        # print(f"Metadata missing for {filename}, skipping.")
                        # lat, lon, photo_datetime = get_image_metadata(image_path)
