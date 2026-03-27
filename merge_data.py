import json
import re

# Read data_auto.js
with open('data_auto.js', 'r', encoding='utf-8') as f:
    auto_content = f.read()
    # Extract json
    json_str = auto_content[auto_content.find('{'):auto_content.rfind('}')+1]
    new_data = json.loads(json_str)

# Read original data.js to get shapes, numbers, letters
with open('data.js', 'r', encoding='utf-8') as f:
    orig_content = f.read()

def extract_array(var_name, content):
    match = re.search(fr"const\s+{var_name}\s*=\s*(\[.*?\]);", content, flags=re.DOTALL)
    if match:
        # Dirty eval of strict JSON-like JS is dangerous, but we just want to copy the raw JS text.
        return match.group(1)
    return "[]"

shapes_arr = extract_array("shapes", orig_content)
numbers_arr = extract_array("numbers", orig_content)
letters_arr = extract_array("letters", orig_content)

# Now rebuild data.js
out_js = f"""// --- 1. 動物森林 (Animals) ---
const animals = {json.dumps(new_data.get('animals', []), ensure_ascii=False, indent=4)};

// --- 2. 交通工具 (Vehicles) ---
const vehicles = {json.dumps(new_data.get('vehicles', []), ensure_ascii=False, indent=4)};

// --- 3. 昆蟲森林 (Insects) ---
const insects = {json.dumps(new_data.get('insects', []), ensure_ascii=False, indent=4)};

// --- 4. 恐龍世界 (Dinosaurs) ---
const dinosaurs = {json.dumps(new_data.get('dinosaurs', []), ensure_ascii=False, indent=4)};

// --- 5. 形狀與圖案 (Shapes) ---
const shapes = {shapes_arr};

// --- 6. 數字學習 (Numbers) ---
const numbers = {numbers_arr};

// --- 7. 英文字母 (Letters) ---
const letters = {letters_arr};

// --- 8. 家中物品 (Household) ---
const household = {json.dumps(new_data.get('household', []), ensure_ascii=False, indent=4)};

// 集中匯出所有資料
const gameData = {{
    animals,
    vehicles,
    insects,
    dinosaurs,
    shapes,
    numbers,
    letters,
    household
}};
"""

with open('data.js', 'w', encoding='utf-8') as f:
    f.write(out_js)

print("Merged data.js successfully.")
