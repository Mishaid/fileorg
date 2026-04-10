import os
import shutil

root_folder = "/mnt/nv2/spacebox/source/python-source/fileorg/test/h"

if os.path.exists(root_folder) == False:
    print("Folder", root_folder, "Does not exist!")
    input("Press Enter to exit...")
    quit()


root_content = os.listdir(root_folder)

for dir in root_content:
    dir_fullpath = os.path.join(root_folder, dir)
    if os.path.isdir(dir_fullpath):
        pdf_sub_dir = os.path.join(dir_fullpath, "pdf")
        kra_sub_dir = os.path.join(dir_fullpath, "kra")
        png_sub_folder = os.path.join(dir_fullpath, "png")

        os.makedirs(pdf_sub_dir, exist_ok=True)
        os.makedirs(kra_sub_dir, exist_ok=True)
        os.makedirs(png_sub_folder, exist_ok=True)

        for file in root_content:
            if "_" + dir in file:
                if "pdf" in file:
                    try:
                        shutil.move(os.path.join(root_folder, file), pdf_sub_dir)
                    except Exception as err:
                        print(err)
                elif "png" in file:
                    try:
                        shutil.move(os.path.join(root_folder, file), png_sub_folder)
                    except Exception as err:
                        print(err)
                elif "kra" in file:
                    try:
                        shutil.move(os.path.join(root_folder, file), kra_sub_dir)
                    except Exception as err:
                        print(err)
            else:
                continue
    else:
        continue

input("Press Enter to exit...")