import os
import shutil
import sys
from pathlib import Path

def project_root(anchor: str = ".git"):
    path = Path.cwd()
    for parent in [path] + list(path.parents):
        if (parent / anchor).exists():
            return parent
    raise FileNotFoundError(
        f"Could not find {anchor} in the parent directories of {path}")

def move_all_files_to_images(images_folders, global_images_folder):
    global_images_folder.mkdir(exist_ok=True)
    for images_folder in images_folders:
        for root, dirs, files in os.walk(images_folder):
            for file in files:
                file_path = Path(root) / file
                if global_images_folder in file_path.parents:
                    continue
                dest_path = global_images_folder / file
                if dest_path.exists():
                    base, ext = os.path.splitext(file)
                    i = 1
                    while (global_images_folder / f"{base}_{i}{ext}").exists():
                        i += 1
                    dest_path = global_images_folder / f"{base}_{i}{ext}"
                shutil.move(str(file_path), str(dest_path))
                print(f"Moved: {file_path} -> {dest_path}")

if __name__ == "__main__":
    ROOT = project_root()
    global_images_folder = ROOT / "Images"

    images_folders = [
        p for p in ROOT.rglob("Images")
        if p.is_dir() and p != global_images_folder
    ]

    if not images_folders:
        print("No images were found in proyects")
        sys.exit(0)

    print("Image folder founds:")
    for folder in images_folders:
        print(f" - {folder}")

    move_all_files_to_images(images_folders, global_images_folder)