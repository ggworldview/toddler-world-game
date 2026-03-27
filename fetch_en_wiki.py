import os
import json
import urllib.request
import urllib.parse
import time

cats = {
    "animals": {"獅子":"Lion", "老虎":"Tiger", "豹":"Leopard", "雪豹":"Snow_leopard", "斑馬":"Zebra", "大猩猩":"Gorilla", "犀牛":"Rhinoceros", "河馬":"Hippopotamus", "長頸鹿":"Giraffe", "水牛":"Water_buffalo", "駱駝":"Camel", "貓熊":"Giant_panda", "無尾熊":"Koala", "袋鼠":"Kangaroo", "狐狸":"Red_fox", "野狼":"Wolf", "貓咪":"Cat", "狗狗":"Dog", "小豬":"Pig", "猴子":"Monkey", "浣熊":"Raccoon", "白馬":"Horse", "小白兔":"Domestic_rabbit", "野兔":"Hare", "老鼠":"Mouse", "倉鼠":"Hamster", "松鼠":"Squirrel", "刺蝟":"Hedgehog", "蝙蝠":"Bat", "乳牛":"Dairy_cattle", "麋鹿":"Moose", "綿羊":"Sheep", "山羊":"Goat", "企鵝":"Penguin", "北極熊":"Polar_bear", "海豹":"Earless_seal", "海龜":"Sea_turtle", "鯊魚":"Shark", "鯨魚":"Whale", "海豚":"Dolphin", "水獺":"Otter"},
    "vehicles": {"汽車":"Car", "計程車":"Taxi", "跑車":"Sports_car", "休旅車":"SUV", "公車":"Bus", "垃圾車":"Garbage_truck", "救護車":"Ambulance", "消防車":"Fire_engine", "大卡車":"Semi-trailer_truck", "拖拉機":"Tractor", "堆高機":"Forklift", "挖土機":"Excavator", "重機":"Motorcycle", "腳踏車":"Bicycle", "滑板車":"Kick_scooter", "滑板":"Skateboard", "蒸汽火車":"Steam_locomotive", "高鐵":"High-speed_rail", "火車":"Train", "捷運":"Rapid_transit", "輕軌":"Tram", "直升機":"Helicopter", "飛機":"Airliner", "戰鬥機":"Fighter_aircraft", "太空梭":"Space_Shuttle", "獨木舟":"Canoe", "帆船":"Sailboat", "郵輪":"Cruise_ship", "潛水艇":"Submarine", "熱氣球":"Hot_air_balloon"},
    "household": {"沙發":"Couch", "椅子":"Chair", "桌子":"Table_(furniture)", "雙人床":"Bed", "大門":"Door", "窗戶":"Window", "電風扇":"Fan_(machine)", "吹風機":"Hair_dryer", "冷氣機":"Air_conditioning", "洗衣機":"Washing_machine", "冰箱":"Refrigerator", "微波爐":"Microwave_oven", "電鍋":"Rice_cooker", "洗碗機":"Dishwasher", "馬桶":"Toilet", "蓮蓬頭":"Shower", "肥皂":"Soap", "牙刷":"Toothbrush", "毛巾":"Towel", "掃把":"Broom", "拖把":"Mop", "垃圾桶":"Waste_container", "電視":"Television", "智慧型手機":"Smartphone", "筆記型電腦":"Laptop", "印表機":"Printer_(computing)", "鎢絲燈泡":"Incandescent_light_bulb", "手電筒":"Flashlight", "鐵鎚":"Hammer", "活動扳手":"Wrench", "滅火器":"Fire_extinguisher"},
    "fruits": {"蘋果":"Apple", "香蕉":"Banana", "橘子":"Mandarin_orange", "葡萄":"Grape", "草莓":"Strawberry", "櫻桃":"Cherry", "藍莓":"Blueberry", "芒果":"Mango", "鳳梨":"Pineapple", "西瓜":"Watermelon", "哈密瓜":"Cantaloupe", "木瓜":"Papaya", "水蜜桃":"Peach", "奇異果":"Kiwifruit", "檸檬":"Lemon", "芭樂":"Guava", "百香果":"Passion_fruit", "火龍果":"Pitaya", "番茄":"Tomato", "高麗菜":"Cabbage", "大白菜":"Napa_cabbage", "花椰菜":"Cauliflower", "綠花椰菜":"Broccoli", "胡蘿蔔":"Carrot", "馬鈴薯":"Potato", "地瓜":"Sweet_potato", "洋蔥":"Onion", "大蒜":"Garlic", "玉米":"Corn", "南瓜":"Pumpkin", "茄子":"Eggplant"},
    "insects": {"蒼蠅":"Housefly", "果蠅":"Drosophila", "蟋蟀":"Cricket_(insect)", "蚱蜢":"Grasshopper", "蚯蚓":"Earthworm", "螳螂":"Mantis", "夏蟬":"Cicada", "蜻蜓":"Dragonfly", "螢火蟲":"Firefly", "蜈蚣":"Centipede", "馬陸":"Millipede", "蠍子":"Scorpion", "獨角仙":"Japanese_rhinoceros_beetle", "鍬形蟲":"Stag_beetle", "椿象":"Pentatomidae"}
}

os.makedirs('assets', exist_ok=True)
data_out = {cat: [] for cat in cats.keys()}

# Resolve wiki image URLs in bulk (50 max per query)
title_to_url = {}

def chunk_dict(d, n):
    items = list(d.items())
    for i in range(0, len(items), n):
        yield dict(items[i:i + n])

all_items_flat = {}
for items in cats.values():
    for zh, en_name in items.items():
        all_items_flat[en_name] = zh

for i, chunk in enumerate(chunk_dict(all_items_flat, 50)):
    titles_str = "|".join([urllib.parse.quote(en) for en in chunk.keys()])
    url = f"https://en.wikipedia.org/w/api.php?action=query&titles={titles_str}&prop=pageimages&format=json&pithumbsize=600&redirects=1&pilimit=50"
    
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    print(f"Fetching bulq query chunk {i+1}...")
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())
            pages = data['query']['pages']
            for page_id, page_data in pages.items():
                if 'title' in page_data and 'thumbnail' in page_data:
                    title = page_data['title'].replace(" ", "_")
                    title_to_url[title] = page_data['thumbnail']['source']
    except Exception as e:
        print(f"Failed chunk {i+1}: {e}")
    time.sleep(1)

success_count = 0
fail_count = 0

# Now sequentially download everything and don't multithread directly if we don't have to,
# since this is fetching real images via direct Wiki upload URLs which are very reliable but let's be safe.
for cat, items in cats.items():
    for zh, en in items.items():
        safe_name = f"e_{cat}_{en}.jpg"
        img_path = os.path.join('assets', safe_name)
        
        url_source = None
        # the title returned by MW API has spaces instead of underscores, and sometimes different case
        for k, v in title_to_url.items():
            if k.lower() == en.lower().replace("_"," "):
                url_source = v
                break

        # Fallback exact match if dict comprehension replaced underscores
        img_url = url_source or title_to_url.get(en.replace("_"," ")) or title_to_url.get(en)
        
        if not img_url:
            print(f"No image URL found for {en} ({zh})")
            fail_count+=1
            continue
            
        if not os.path.exists(img_path):
            try:
                req = urllib.request.Request(img_url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req, timeout=10) as resp, open(img_path, 'wb') as f:
                    f.write(resp.read())
            except Exception as e:
                print(f"Failed to download {zh} ({en}): {e}")
                fail_count+=1
                continue
        
        data_out[cat].append({"img": f"./assets/{safe_name}", "name": zh})
        success_count += 1
        time.sleep(0.1) # small delay just in case

print(f"Downloaded {success_count} images, {fail_count} failed.")

# Preserve the flawless 17 AI arts
data_out["dinosaurs"] = [
    {"img": "./assets/dino_trex.png", "name": "暴龍"},
    {"img": "./assets/dino_brachiosaurus.png", "name": "腕龍"},
    {"img": "./assets/dino_stegosaurus.png", "name": "劍龍"},
    {"img": "./assets/dino_triceratops.png", "name": "三角龍"},
    {"img": "./assets/dino_pteranodon.png", "name": "翼龍"}
]
ai_insects = {"毛毛蟲":"caterpillar", "蝴蝶":"butterfly", "蝸牛":"snail", "瓢蟲":"ladybug", "螞蟻":"ant", "蜜蜂":"bee", "甲蟲":"beetle", "蟑螂":"cockroach", "蜘蛛":"spider", "蜘蛛網":"spiderweb", "蚊子":"mosquito"}
data_out["insects"] = [{"img": f"./assets/insect_{v}.png", "name": k} for k, v in ai_insects.items()] + data_out["insects"]

with open('data_final.json', 'w', encoding='utf-8') as f:
    json.dump(data_out, f, ensure_ascii=False)
