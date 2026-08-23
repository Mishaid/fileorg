import os, shutil, time

root_folder = "/home/mishaid/spacebox/source/python/fileorg/test"
# root_folder = "C:\\Users\\aksel\\OneDrive\\Рабочий стол\\123"

os.chdir(root_folder)

folders = [folder for folder in os.listdir('.') if os.path.isdir(folder)]

while True:
    for folder in folders:
        os.chdir(os.path.join(root_folder, folder))
        files = [file for file in os.listdir('.') if os.path.isfile(file)]
        for file in files:
            ext = file.split('.')[-1]
            os.makedirs(ext, exist_ok=True)
            shutil.move(file, os.path.join(file.split('.')[-1], file))
        print(files)
    time.sleep(15)