import os
from PIL import Image #!compiler_ignore

def process_directory(directory):
    for entry in os.scandir(directory):
        if entry.is_file() and entry.name.endswith(".png"):
            print(entry.name)
            img = Image.open(entry.path)
            img = img.resize((img.width * 2, img.height * 2), Image.NEAREST)
            img.save(entry.path)
        elif entry.is_dir():
            process_directory(entry.path)

process_directory("split")
