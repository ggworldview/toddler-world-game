import json
import re
import os

with open('data_final.json', 'r', encoding='utf-8') as f:
    new_data = json.load(f)

with open('data.js', 'r', encoding='utf-8') as f:
    orig_content = f.read()

def extract_array(var_name, content):
    match = re.search(fr"const\s+{var_name}\s*=\s*(\[.*?\]);", content, flags=re.DOTALL)
    return match.group(1) if match else "[]"

shapes_arr = extract_array("shapes", orig_content)
numbers_arr = extract_array("numbers", orig_content)
letters_arr = extract_array("letters", orig_content)

out_js = f"""// --- DDG/Wiki High Quality Data Compilation ---
const animals = {json.dumps(new_data.get('animals', []), ensure_ascii=False, indent=4)};
const vehicles = {json.dumps(new_data.get('vehicles', []), ensure_ascii=False, indent=4)};
const insects = {json.dumps(new_data.get('insects', []), ensure_ascii=False, indent=4)};
const dinosaurs = {json.dumps(new_data.get('dinosaurs', []), ensure_ascii=False, indent=4)};
const household = {json.dumps(new_data.get('household', []), ensure_ascii=False, indent=4)};
const fruits = {json.dumps(new_data.get('fruits', []), ensure_ascii=False, indent=4)};

const shapes = {shapes_arr};
const numbers = {numbers_arr};
const letters = {letters_arr};

const gameData = {{
    animals, vehicles, insects, dinosaurs,
    shapes, numbers, letters,
    household, fruits
}};
"""

with open('data.js', 'w', encoding='utf-8') as f:
    f.write(out_js)

print("data.js successfully built with En Wiki high quality images!")
