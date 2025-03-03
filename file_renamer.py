import os
import config
from metadata_extractor import get_image_metadata, format_metadata
from unique_filename_generator import generate_unique_suffix
import shutil
from file_validation import validate_file



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


def generate_report_html(audio_files_count, other_files_count, video_files_count, updated_files_count, edited_files_count, output_html="file_report.html"):
    """Generates an HTML report of file counts."""
    total_processed = audio_files_count + other_files_count + video_files_count + updated_files_count + edited_files_count

    html_content = f"""
<!DOCTYPE html>
    <html>
    <head>
        <title>File Processing Report</title>
        <style>
            body {{ font-family: 'Arial', sans-serif; background-color: #f4f4f4; color: #333; margin: 20px; }}
            h1, h2 {{ color: #007bff; text-align: center; margin-bottom: 20px; }}
            table {{ border-collapse: collapse; width: 80%; margin: 20px auto; background-color: white; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); border-radius: 8px; overflow: hidden; }}
            th, td {{ border: 1px solid #ddd; padding: 12px 15px; text-align: left; }}
            th {{ background-color: #007bff; color: white; font-weight: bold; }}
            tr:nth-child(even) {{ background-color: #f9f9f9; }}
            tr:hover {{ background-color: #e0f7fa; }}
            p {{ line-height: 1.6; margin-bottom: 15px; padding: 10px; background-color: #e8f5e9; border-radius: 5px; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05); }}
        </style>
    </head>
    <body>
        <h1>File Processing Report</h1>
        <h2>Total Files Processed</h2>
        <p>Total: {total_processed}</p>
        <h2>File Type Counts</h2>
        <table>
            <tr><th>File Type</th><th>Count</th></tr>
            <tr><td>Updated Images</td><td>{updated_files_count}</td></tr>
            <tr><td>Audio</td><td>{audio_files_count}</td></tr>
            <tr><td>Video</td><td>{video_files_count}</td></tr>
            <tr><td>Edited</td><td>{edited_files_count}</td></tr>
            <tr><td>Other types of documents</td><td>{other_files_count}</td></tr>
        </table>
        <h2>Edited Files (Metadata Issues)</h2>
        <p>Files with metadata issues or any other problem extracting those date: {edited_files_count}</p>
        <p>Those files are images.</p>
        <h2>Mapped Files (Geo-Tagged)</h2>
        <p>Files mapped with geolocation data on the generated html map: {updated_files_count}</p>
    </body>
    </html>
    """
    full_output_path = os.path.join(config.OUTPUT_PATH, output_html) #combine the folder and file name.

    with open(full_output_path, "w") as f:
        f.write(html_content)

    print(f"Report generated: {output_html}")

