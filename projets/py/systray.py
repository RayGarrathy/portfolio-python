import pystray
from PIL import Image
import sys
import os

def open_file(path):
    try:
        import subprocess
        subprocess.Popen(["start", "", path], shell=True)
    except Exception as e:
        print(f"Erreur ouverture {path}: {e}")

def make_callback(path):
    def callback(icon, item):
        open_file(path)
    return callback

def build_submenu_from_folder(folder_path, emoji="📊"):
    items = []
    if os.path.exists(folder_path):
        for filename in os.listdir(folder_path):
            full_path = os.path.join(folder_path, filename)
            if filename.lower().endswith((".xlsx", ".xls", ".lnk")):
                display_name = f"{emoji} {os.path.splitext(filename)[0]}"
                items.append(pystray.MenuItem(display_name, make_callback(full_path)))
    else:
        items.append(pystray.MenuItem("⚠️ Dossier introuvable", lambda icon, item: None))
    return pystray.Menu(*items)

def quit_program(icon, item):
    icon.stop()
    sys.exit(0)

# --- Sous-menus dynamiques ---
submenu_cc         = build_submenu_from_folder(r"Z:\CC", "📊")
submenu_dossier    = build_submenu_from_folder(r"Z:\Dossier", "📁")
submenu_masques    = build_submenu_from_folder(r"Z:\Masques", "📑")
submenu_planning   = build_submenu_from_folder(r"Z:\Planning", "📅")
submenu_reception  = build_submenu_from_folder(r"Z:\Réception-DA", "📥")

menu = pystray.Menu(
    pystray.MenuItem("CC", submenu_cc),
    pystray.MenuItem("Dossier", submenu_dossier),
    pystray.MenuItem("Masques", submenu_masques),
    pystray.MenuItem("Planning", submenu_planning),
    pystray.MenuItem("Réception-DA", submenu_reception),
    pystray.MenuItem("Quitter", quit_program)
)

# --- Utilisation du fichier .ico ---
icon_path = r"C:\Users\jm218850\AppData\Local\Programs\Python\Python311\Fichiers python\Systray\icone.ico"
icon = pystray.Icon("MonProgramme", Image.open(icon_path), "Menu Excel", menu)

if __name__ == "__main__":
    icon.run()
