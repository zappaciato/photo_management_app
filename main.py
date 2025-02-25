import os
from map_generator import create_photo_map

if __name__ == "__main__":
    folder_path = r"C:\Users\kflakiewicz\Desktop\Media_Kris\GeoPhoto_app\Photos"
    output_directory = r"C:\Users\kflakiewicz\Desktop\Media_Kris\GeoPhoto_app\Photos"
    create_photo_map(folder_path, output_directory)