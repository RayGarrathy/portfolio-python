import time
import os
from pathlib import Path
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
from winotify import Notification

# Dossier réseau à surveiller
DOSSIER_A_SURVEILLER = r""

class Handler(FileSystemEventHandler):
    
    def on_created(self, event):
        if not event.is_directory:
            file = Path(event.src_path).name
            dir_name = os.path.basename(os.path.dirname(event.src_path))

            notif = Notification(
                app_id=f"Notification {dir_name}",
                title="Un nouveau rapport est disponible",
                msg=file,
                duration="short",
                icon=r"C:\ProgramData\SurveillanceDossier\papier.ico"
            )

            notif.add_actions(
                label=f"Ouvrir {dir_name}",
                launch=os.path.dirname(event.src_path)
            )

            notif.show()

def main():
    observer = Observer()
    observer.schedule(Handler(), DOSSIER_A_SURVEILLER, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()

if __name__ == "__main__":
    main()
