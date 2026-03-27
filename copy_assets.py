import os
import shutil
import re

src_dir = r"C:\Users\ggwor\.gemini\antigravity\brain\6577c61b-ddd4-414b-a22a-8a0bcbe63f70"
dest_dir = r"C:\Users\ggwor\Documents\Antigravity dev spcae\assets"

os.makedirs(dest_dir, exist_ok=True)

for file in os.listdir(src_dir):
    if file.startswith("dino_") or file.startswith("insect_"):
        clean_name = re.sub(r'_\d+\.png$', '.png', file)
        src_path = os.path.join(src_dir, file)
        dest_path = os.path.join(dest_dir, clean_name)
        shutil.copy2(src_path, dest_path)
        print("Copied:", clean_name)
