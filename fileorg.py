from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time, os, shutil, sys, logging

home_dir = os.path.expanduser('~')
LOG_FILE_PATH = os.path.join(home_dir, 'FileOrg', 'fileorg.log')

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filename=LOG_FILE_PATH, filemode="a", encoding='utf-8')

if sys.platform.startswith('win'):
    sep = '\\'
    CONFIG_PATH = home_dir + '\\FileOrg\\dirs.txt'
    CONFIG_DIR = home_dir + '\\FileOrg'
    win = True
elif sys.platform.startswith('linux'):
    sep = '/'
    CONFIG_PATH = home_dir + '/FileOrg/dirs.txt'
    CONFIG_DIR = home_dir + '/FileOrg'
    win = False
else:
    print('Start on unsupported OS!')
    exit(1)


#Config loader
def load_config(dir_observer) -> None:
    global CONFIG_PATH
    dir_observer.unschedule_all()
    with open(CONFIG_PATH, 'r', encoding='utf-8') as file:
        directories = file.read().splitlines()
    for d in directories:
        dir_observer.schedule(Handler(), path=d, recursive=False)

# New file mover
def file_mover(path: str) -> None:
    full_path = path.split(sep)
    if win == True:
        directory = os.path.join(full_path[0] + '\\', *full_path[1:-1])
    else:
        directory = os.path.join(sep, *full_path[:-1])
    filename = full_path[-1]
    ext = filename.split('.')[-1]
    os.chdir(directory)
    os.makedirs(ext, exist_ok=True)
    shutil.move(filename, os.path.join(ext, filename))


# Config update handler
class ConfigObserver(FileSystemEventHandler):
    def __init__(self, dir_observer) -> None:
        self.dir_observer = dir_observer

    def on_modified(self, event) -> None:
        global CONFIG_PATH
        if not event.is_directory:
            if os.path.basename(event.src_path) == os.path.basename(CONFIG_PATH):
                print(f'config {os.path.basename(event.src_path)} modified!')
                logging.info(f'config {os.path.basename(event.src_path)} modified!')
                load_config(self.dir_observer)

    def on_moved(self, event) -> None:
        global CONFIG_PATH
        if not event.is_directory:
            if os.path.basename(event.dest_path) == os.path.basename(CONFIG_PATH):
                print(f'config {os.path.basename(event.dest_path)} modified!')
                logging.info(f'config {os.path.basename(event.dest_path)} modified!')
                load_config(self.dir_observer)

# New files handler
class Handler(FileSystemEventHandler):
    def on_created(self, event) -> None:
        if not event.is_directory:
            print(f"New File: {event.src_path}")
            logging.info(f"New File: {event.src_path}")
            time.sleep(0.5)
            file_mover(str(event.src_path))


# Dirs handler initialization
dir_observer = Observer()
load_config(dir_observer)
dir_observer.start()

# Config handler initiallization
config_observer = Observer()
config_observer.schedule(ConfigObserver(dir_observer), path=CONFIG_DIR, recursive=False)
config_observer.start()


# Main cycle
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    dir_observer.stop()
    config_observer.stop()
dir_observer.join()
config_observer.join()