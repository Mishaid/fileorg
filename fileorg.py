import time, os, shutil, logging

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

home_dir = os.path.expanduser('~')
LOG_FILE_PATH = os.path.join(home_dir, 'FileOrg', 'fileorg.log')

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filename=LOG_FILE_PATH, filemode="a", encoding='utf-8')

CONFIG_PATH = os.path.join(home_dir, 'FileOrg', 'dirs.txt')
CONFIG_DIR = os.path.join(home_dir, 'FileOrg')

#Config loader
def load_config(dir_observer) -> None:
    global CONFIG_PATH

    dir_observer.unschedule_all()

    if not os.path.exists(CONFIG_PATH):
        print(f"Config file does not exist: {CONFIG_PATH}")
        logging.warning(f"Config file does not exist: {CONFIG_PATH}")
        return

    with open(CONFIG_PATH, 'r', encoding='utf-8') as file:
        directories = file.read().splitlines()

    for d in directories:
        if not os.path.isdir(d):
            logging.warning(f"Directory does not exist: {d}")
            continue
        dir_observer.schedule(Handler(), path=d, recursive=False)
        logging.info(f"Watching directory: {d}")

# New file mover
def file_mover(path: str):

    directory = os.path.dirname(path)
    filename = os.path.basename(path)

    # get file extension
    _, extension = os.path.splitext(filename)
    extension = extension.lstrip(".")
    if not extension:
        extension = "no_extension"

    destination_directory = os.path.join(directory,extension)
    os.makedirs(destination_directory, exist_ok=True)
    destination = os.path.join(destination_directory, filename)
    shutil.move(path, destination)

    logging.info(f"Moved: {path} -> {destination}")


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
            try:
                file_mover(str(event.src_path))

            except Exception:
                print(f"Failed to move file: {event.src_path}")
                logging.exception(f"Failed to move file: {event.src_path}")


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