import os
import shutil

root_folder = "/mnt/nv2/spacebox/source/python-source/fileorg/test/h"
# root_folder = "C:\\Users\\aksel\\OneDrive\\Рабочий стол\\123"

if os.path.exists(root_folder) == False:
    print("Folder", root_folder, "Does not exist!")
    input("Press Enter to exit...")
    quit()


root_content = os.listdir(root_folder)
root_dirs = []
root_files = []

for item in root_content:
    item_fullpath = os.path.join(root_folder, item)
    if os.path.isdir(item_fullpath):
        root_dirs.append(item)
    elif os.path.isfile(item_fullpath):
        root_files.append(item)

for file in root_files:
    for dir in root_dirs:
        if dir in file and "_" + dir in file:
            dir_fullpath = os.path.join(root_folder, dir)
            if "png" in file:
                try:
                    png_sub_folder = os.path.join(dir_fullpath, "png")
                    os.makedirs(png_sub_folder, exist_ok=True)
                    shutil.move(os.path.join(root_folder, file), png_sub_folder)
                except Exception as err:
                    print(err)
            elif "kra" in file:
                try:
                    kra_sub_dir = os.path.join(dir_fullpath, "kra")
                    os.makedirs(kra_sub_dir, exist_ok=True)
                    shutil.move(os.path.join(root_folder, file), kra_sub_dir)
                except Exception as err:
                    print(err)
            else:
                continue

input("Press Enter to exit...")