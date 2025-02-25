import os
from map_generator import create_photo_map
from file_renamer import rename_files

if __name__ == "__main__":
    folder_path = r"C:\Users\kflakiewicz\Desktop\Media_Kris\GeoPhoto_app\Photos"
    output_path = r"C:\Users\kflakiewicz\Desktop\Media_Kris\GeoPhoto_app\Photos"
    rename_files(folder_path, output_path)
    create_photo_map(folder_path, output_path)
