import os
import config
from map_generator import create_photo_map
from file_renamer import rename_files

# from config import OUTPUT_PATH


if __name__ == "__main__":

    rename_files(config.UTILITY_BASE_FOLDER_PATH, config.OUTPUT_PATH)
    create_photo_map(config.UPDATED_PHOTOS_PATH, config.OUTPUT_PATH)



  