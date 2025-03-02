import os
from map_generator import create_photo_map
from file_renamer import rename_files

if __name__ == "__main__":
    folder_path = r"C:\Users\kflakiewicz\Desktop\Media_Kris\FOTO\GeoPhoto_app\Photos"
    output_path = r"C:\Users\kflakiewicz\Desktop\Media_Kris\FOTO\GeoPhoto_app\RESULT"

    rename_files(folder_path, output_path)
    create_photo_map(output_path)


    #robi tylko dwa thumnails.. trzeba zmienic troche i potestowac 
