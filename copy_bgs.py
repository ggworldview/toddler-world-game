import os
import shutil

artifact_dir = r"C:\Users\ggwor\.gemini\antigravity\brain\6577c61b-ddd4-414b-a22a-8a0bcbe63f70"
bg_dir = r"assets\backgrounds"
os.makedirs(bg_dir, exist_ok=True)

prefixes = [
    "bg_savanna", "bg_forest", "bg_desert", "bg_plains",
    "bg_airport", "bg_city", "bg_farm", "bg_highway",
    "bg_leaf", "bg_garden", "bg_treetrunk", "bg_volcano",
    "bg_jungle", "bg_river", "bg_pastel", "bg_chalkboard", 
    "bg_starry", "bg_classroom", "bg_math", "bg_library", 
    "bg_nursery", "bg_livingroom", "bg_bedroom", "bg_kitchen"
]

for prefix in prefixes:
    files = [f for f in os.listdir(artifact_dir) if f.startswith(prefix) and f.endswith(".png")]
    if files:
        files.sort(key=lambda x: os.path.getmtime(os.path.join(artifact_dir, x)), reverse=True)
        latest_file = files[0]
        shutil.copy2(os.path.join(artifact_dir, latest_file), os.path.join(bg_dir, f"{prefix}.png"))
        print(f"Copied {latest_file} to {prefix}.png")
