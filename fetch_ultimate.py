import os
import json
import urllib.request
import urllib.parse
import time
import re

mapping = {
    "animals": {
        "獅子": "Lion", "老虎": "Tiger", "豹": "Leopard", "雪豹": "Snow leopard", "美洲獅": "Cougar", "獵豹": "Cheetah", "斑馬": "Zebra", "大猩猩": "Gorilla", "紅毛猩猩": "Orangutan", "犀牛": "Rhinoceros",
        "河馬": "Hippopotamus", "長頸鹿": "Giraffe", "水牛": "Water buffalo", "駱駝": "Camel", "羊駝": "Alpaca", "貓熊": "Giant panda", "無尾熊": "Koala", "袋鼠": "Kangaroo", "狐狸": "Red fox", "野狼": "Wolf",
        "貓咪": "Cat", "狗狗": "Dog", "小豬": "Pig", "猴子": "Monkey", "狒狒": "Baboon", "黑猩猩": "Chimpanzee", "浣熊": "Raccoon", "白馬": "Horse", "棕馬": "Mustang", "小白兔": "Rabbit",
        "野兔": "Hare", "老鼠": "Mouse", "倉鼠": "Hamster", "天竺鼠": "Guinea pig", "松鼠": "Squirrel", "刺蝟": "Hedgehog", "蝙蝠": "Bat", "乳牛": "Dairy cattle", "鹿": "Deer", "麋鹿": "Moose",
        "綿羊": "Sheep", "山羊": "Goat", "企鵝": "Penguin", "北極熊": "Polar bear", "海豹": "Earless seal", "海龜": "Sea turtle", "鯊魚": "Shark", "鯨魚": "Whale", "海豚": "Dolphin", "水獺": "Otter"
    },
    "vehicles": {
        "汽車": "Car", "計程車": "Taxi", "休旅車": "SUV", "跑車": "Sports car", "吉普車": "Jeep", "電動車": "Electric car", "公車": "Bus", "遊覽車": "Coach (bus)", "娃娃車": "School bus", "垃圾車": "Garbage truck",
        "郵務車": "Mail truck", "警用汽車": "Police car", "救護車": "Ambulance", "消防車": "Fire engine", "大貨車": "Truck", "貨櫃車": "Semi-trailer truck", "拖吊車": "Tow truck", "拖拉機": "Tractor", "堆高機": "Forklift", "挖土機": "Excavator",
        "推土機": "Bulldozer", "水泥車": "Concrete mixer", "砂石車": "Dump truck", "重機": "Motorcycle", "野狼機車": "Cruiser (motorcycle)", "腳踏車": "Bicycle", "電動自行車": "Electric bicycle", "滑板車": "Kick scooter", "滑板": "Skateboard", "蒸汽火車": "Steam locomotive",
        "高鐵": "High-speed rail", "火車": "Train", "捷運": "Rapid transit", "輕軌電車": "Tram", "直升機": "Helicopter", "小飛機": "Light aircraft", "客機": "Airliner", "戰鬥機": "Fighter aircraft", "太空梭": "Space Shuttle", "太空火箭": "Rocket",
        "獨木舟": "Canoe", "帆船": "Sailboat", "快艇": "Motorboat", "水上摩托車": "Personal watercraft", "橡皮艇": "Inflatable boat", "豪華郵輪": "Cruise ship", "渡輪": "Ferry", "潛水艇": "Submarine", "熱氣球": "Hot air balloon", "纜車": "Aerial tramway"
    },
    "household": {
        "沙發": "Couch", "茶几": "Coffee table", "木頭椅子": "Chair", "餐椅": "Folding chair", "餐桌": "Table (furniture)", "書桌": "Desk", "雙人床": "Bed", "嬰兒床": "Infant bed", "衣櫃": "Wardrobe", "鞋櫃": "Shoe rack",
        "大門": "Door", "全身鏡": "Mirror", "玻璃窗": "Window", "電風扇": "Mechanical fan", "吹風機": "Hair dryer", "冷氣機": "Air conditioning", "除濕機": "Dehumidifier", "洗衣機": "Washing machine", "冰箱": "Refrigerator", "微波爐": "Microwave oven",
        "烤箱": "Oven", "瓦斯爐": "Kitchen stove", "抽油煙機": "Kitchen hood", "熱水瓶": "Electric water boiler", "電鍋": "Rice cooker", "洗碗機": "Dishwasher", "馬桶": "Toilet", "浴缸": "Bathtub", "蓮蓬頭": "Shower", "肥皂": "Soap",
        "洗髮乳": "Shampoo", "牙刷": "Toothbrush", "牙膏": "Toothpaste", "毛巾": "Towel", "掃把": "Broom", "拖把": "Mop", "垃圾桶": "Waste container", "鬧鐘": "Alarm clock", "液晶電視": "Television", "智慧型手機": "Smartphone",
        "筆記型電腦": "Laptop", "桌上型電腦": "Desktop computer", "印表機": "Printer (computing)", "電源插座": "AC power plugs and sockets", "鎢絲燈泡": "Incandescent light bulb", "手電筒": "Flashlight", "鐵鎚": "Hammer", "活動扳手": "Wrench", "螺絲起子": "Screwdriver", "滅火器": "Fire extinguisher"
    },
    "fruits": {
        "蘋果": "Apple", "香蕉": "Banana", "橘子": "Mandarin orange", "柳丁": "Orange (fruit)", "葡萄": "Grape", "草莓": "Strawberry", "櫻桃": "Cherry", "藍莓": "Blueberry", "芒果": "Mango", "鳳梨": "Pineapple",
        "西瓜": "Watermelon", "哈密瓜": "Cantaloupe", "木瓜": "Papaya", "水蜜桃": "Peach", "奇異果": "Kiwifruit", "檸檬": "Lemon", "酪梨": "Avocado", "芭樂": "Guava", "百香果": "Passion fruit", "蓮霧": "Syzygium samarangense",
        "火龍果": "Pitaya", "柿子": "Persimmon", "柚子": "Pomelo", "釋迦": "Sugar-apple", "番茄": "Tomato", "高麗菜": "Cabbage", "大白菜": "Napa cabbage", "青江菜": "Bok choy", "空心菜": "Water spinach", "菠菜": "Spinach",
        "花椰菜": "Cauliflower", "綠花椰菜": "Broccoli", "胡蘿蔔": "Carrot", "白蘿蔔": "Daikon", "馬鈴薯": "Potato", "地瓜": "Sweet potato", "芋頭": "Taro", "洋蔥": "Onion", "大蒜": "Garlic", "青蔥": "Scallion",
        "芹菜": "Celery", "蘆筍": "Asparagus", "玉米": "Corn", "小黃瓜": "Cucumber", "大黃瓜": "Cucumis sativus", "南瓜": "Pumpkin", "苦瓜": "Bitter melon", "冬瓜": "Wax gourd", "茄子": "Eggplant", "青椒": "Bell pepper"
    },
    "insects": {
        "蒼蠅": "Housefly", "果蠅": "Drosophila", "小黑蚊": "Forcipomyia taiwana", "蟋蟀": "Cricket (insect)", "蚱蜢": "Grasshopper", "蚯蚓": "Earthworm", "螳螂": "Mantis", "夏蟬": "Cicada", "蜻蜓": "Dragonfly", "螢火蟲": "Firefly",
        "蜈蚣": "Centipede", "馬陸": "Millipede", "蜘蛛": "Spider", "蠍子": "Scorpion", "毛毛蟲": "Caterpillar", "蠶寶寶": "Bombyx mori", "大白斑蝶": "Idea leuconoe", "鳳蝶": "Swallowtail butterfly", "飛蛾": "Moth", "蝸牛": "Snail",
        "蛞蝓": "Slug", "瓢蟲": "Coccinellidae", "螞蟻": "Ant", "紅火蟻": "Red imported fire ant", "白蟻": "Termite", "蜜蜂": "Bee", "虎頭蜂": "Hornet", "獨角仙": "Japanese rhinoceros beetle", "鍬形蟲": "Stag beetle", "金龜子": "Scarab beetle"
    },
    "dinosaurs": {
        "暴龍": "Tyrannosaurus", "腕龍": "Brachiosaurus", "劍龍": "Stegosaurus", "三角龍": "Triceratops", "翼龍": "Pteranodon", "迅猛龍": "Velociraptor", "副櫛龍": "Parasaurolophus", "甲龍": "Ankylosaurus", "棘龍": "Spinosaurus", "雷龍": "Brontosaurus",
        "厚頭龍": "Pachycephalosaurus", "蛇頸龍": "Plesiosauria", "魚龍": "Ichthyosaur", "滄龍": "Mosasaurus", "竊蛋龍": "Oviraptor", "慈母龍": "Maiasaura", "異特龍": "Allosaurus", "圓角龍": "Protoceratops", "重爪龍": "Baryonyx", "梁龍": "Diplodocus"
    }
}

os.makedirs('assets', exist_ok=True)
game_data = {k: [] for k in mapping.keys()}
headers = {"User-Agent": "AntigravityBot/1.0 (dev@antigravity.local)"}

for cat, items in mapping.items():
    for zh, en in items.items():
        safe_name = f"z_{cat}_{zh}.jpg"
        img_path = os.path.join("assets", safe_name)
        
        # We enforce fetching images using generator=search to perfectly resolve the exact matched article thumbnail
        url = f"https://en.wikipedia.org/w/api.php?action=query&generator=search&gsrsearch={urllib.parse.quote(en)}&gsrlimit=1&prop=pageimages&pithumbsize=600&format=json"
        
        if not os.path.exists(img_path):
            try:
                req = urllib.request.Request(url, headers=headers)
                with urllib.request.urlopen(req, timeout=5) as resp:
                    data = json.loads(resp.read().decode())
                    if 'query' in data and 'pages' in data['query']:
                        pages = data['query']['pages']
                        page_id = list(pages.keys())[0]
                        if 'thumbnail' in pages[page_id]:
                            img_url = pages[page_id]['thumbnail']['source']
                            # Download the image
                            img_req = urllib.request.Request(img_url, headers=headers)
                            with urllib.request.urlopen(img_req, timeout=10) as iresp, open(img_path, 'wb') as f:
                                f.write(iresp.read())
            except Exception as e:
                pass
            time.sleep(0.05)
            
        # Add to dictionary if download succeeded or file already exists
        if os.path.exists(img_path) and os.path.getsize(img_path) > 100:
            game_data[cat].append({"img": f"./assets/{safe_name}", "name": zh})

# Append AI generated pre-existing SVGs into the front
for dino in [{"img": "./assets/dino_trex.png", "name": "暴龍"}, {"img": "./assets/dino_brachiosaurus.png", "name": "腕龍"}, {"img": "./assets/dino_stegosaurus.png", "name": "劍龍"}, {"img": "./assets/dino_triceratops.png", "name": "三角龍"}, {"img": "./assets/dino_pteranodon.png", "name": "翼龍"}]:
    # Replace if exists
    game_data["dinosaurs"] = [d for d in game_data["dinosaurs"] if d["name"] != dino["name"]]
    game_data["dinosaurs"].insert(0, dino)
    
ai_insects_map = {"毛毛蟲":"caterpillar", "蝴蝶":"butterfly", "蝸牛":"snail", "瓢蟲":"ladybug", "螞蟻":"ant", "蜜蜂":"bee", "甲蟲":"beetle", "蟑螂":"cockroach", "蜘蛛":"spider", "蜘蛛網":"spiderweb", "蚊子":"mosquito"}
for k, v in ai_insects_map.items():
    if os.path.exists(f"assets/insect_{v}.png"):
        game_data["insects"] = [i for i in game_data["insects"] if i["name"] != k]
        game_data["insects"].insert(0, {"img": f"./assets/insect_{v}.png", "name": k})

# Read remaining properties shapes, numbers, letters from data.js
with open('data.js', 'r', encoding='utf-8') as f:
    orig = f.read()
    
def get_arr(var):
    m = re.search(fr"const\s+{var}\s*=\s*(\[.*?\]);", orig, flags=re.DOTALL)
    return m.group(1) if m else "[]"
    
out_js = f"""
const animals = {json.dumps(game_data['animals'], ensure_ascii=False, indent=4)};
const vehicles = {json.dumps(game_data['vehicles'], ensure_ascii=False, indent=4)};
const household = {json.dumps(game_data['household'], ensure_ascii=False, indent=4)};
const fruits = {json.dumps(game_data['fruits'], ensure_ascii=False, indent=4)};
const insects = {json.dumps(game_data['insects'], ensure_ascii=False, indent=4)};
const dinosaurs = {json.dumps(game_data['dinosaurs'], ensure_ascii=False, indent=4)};
const shapes = {get_arr('shapes')};
const numbers = {get_arr('numbers')};
const letters = {get_arr('letters')};

const gameData = {{ animals, vehicles, household, fruits, insects, dinosaurs, shapes, numbers, letters }};
"""

with open('data.js', 'w', encoding='utf-8') as f:
    f.write(out_js)

print("SUCCESS: Full database updated.")
for k, v in game_data.items():
    print(f"[{k}] => {len(v)} items")
