from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time, os ,shutil

class Handler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            print(f"Новый файл: {event.src_path}")
            full_path = event.src_path.split('/')
            directory = os.path.join('/', *full_path[:-1])
            filename = full_path[-1]
            ext = filename.split('.')[-1]
            os.chdir(directory)
            os.makedirs(ext, exist_ok=True)
            shutil.move(filename, os.path.join(ext, filename))
            

observer = Observer()
with open('dirs.txt', 'r', encoding='utf-8') as file:
    directories = file.read().splitlines()
for d in directories:
    observer.schedule(Handler(), path=d, recursive=False)
observer.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()
observer.join()