import urllib.request
import urllib.parse
import json
import os
import time
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

items = {
    "animals": ["獅子", "老虎", "豹", "斑馬", "大猩猩", "紅毛猩猩", "犀牛", "河馬", "長頸鹿", "水牛", "駱駝", "貓熊", "無尾熊", "袋鼠", "狐狸", "野狼", "貓咪", "狗狗", "小豬", "猴子", "白馬", "小白兔", "老鼠", "倉鼠", "松鼠", "刺蝟", "蝙蝠", "乳牛", "鹿", "綿羊", "羊駝", "企鵝", "老鷹", "鴨子", "天鵝", "紅鶴", "孔雀", "鸚鵡", "貓頭鷹", "青蛙", "鱷魚", "烏龜", "蛇", "海豚", "鯨魚", "章魚"],
    "vehicles": ["汽車", "計程車", "休旅車", "公車", "賽車", "警用汽車", "救護車", "消防車", "大貨車", "拖拉機", "重型機車", "腳踏車", "滑板車", "滑板", "蒸汽火車", "高鐵", "捷運", "輕軌", "直升機", "客機", "太空火箭", "獨木舟", "帆船", "快艇", "豪華郵輪", "渡輪", "挖土機", "水泥車", "砂石車"],
    "insects": ["蒼蠅", "蟋蟀", "蚯蚓", "螳螂", "蟬", "蜻蜓", "螢火蟲", "蜈蚣"],
    "household": ["椅子", "沙發", "彈簧床", "大門", "化妝鏡", "窗戶", "馬桶", "浴缸", "蓮蓬頭", "衛生紙", "肥皂", "海綿", "牙刷", "掃把", "水庫", "鑰匙", "泰迪熊", "時鐘", "鬧鐘", "液晶電視", "收音機", "智慧型手機", "筆記型電腦", "電腦螢幕", "印表機", "滑鼠", "電源插座", "鎢絲燈泡", "手電筒", "蠟燭", "書", "筆記本", "鉛筆", "剪刀", "垃圾桶", "鐵鎚", "活動扳手", "螺絲起子", "鋸子", "木梯", "滅火器"]
}

def fetch_wiki_image(keyword):
    # Use generator=search to robustly find the most relevant wiki article
    url = f"https://zh.wikipedia.org/w/api.php?action=query&generator=search&gsrsearch={urllib.parse.quote(keyword)}&gsrlimit=1&prop=pageimages&format=json&pithumbsize=600"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            if 'query' not in data or 'pages' not in data['query']: return None
            pages = data['query']['pages']
            page_id = list(pages.keys())[0]
            if 'thumbnail' in pages[page_id]:
                return pages[page_id]['thumbnail']['source']
    except Exception as e:
        print(f"Error fetching metadata for {keyword}: {e}")
    return None

os.makedirs('assets', exist_ok=True)
data_out = {}
success_count = 0

for category, names in items.items():
    data_out[category] = []
    for name in names:
        img_url = fetch_wiki_image(name)
        if img_url:
            safe_name = f"real_{category}_{name}.jpg"
            img_path = os.path.join('assets', safe_name)
            print(f"Downloading [{name}]...")
            try:
                req = urllib.request.Request(img_url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req) as response, open(img_path, 'wb') as out_file:
                    out_file.write(response.read())
                data_out[category].append({"img": f"./assets/{safe_name}", "name": name})
                success_count += 1
            except Exception as e:
                print(f"Failed to DL {name}: {e}")
        time.sleep(0.1)

# Include the AI Dinosaurs generated earlier
data_out["dinosaurs"] = [
    {"img": "./assets/dino_trex.png", "name": "暴龍"},
    {"img": "./assets/dino_brachiosaurus.png", "name": "腕龍"},
    {"img": "./assets/dino_stegosaurus.png", "name": "劍龍"},
    {"img": "./assets/dino_triceratops.png", "name": "三角龍"},
    {"img": "./assets/dino_pteranodon.png", "name": "翼龍"}
]

# Merge the AI Insects generated earlier
ai_insects = [
    {"img": "./assets/insect_caterpillar.png", "name": "毛毛蟲"},
    {"img": "./assets/insect_butterfly.png", "name": "蝴蝶"},
    {"img": "./assets/insect_snail.png", "name": "蝸牛"},
    {"img": "./assets/insect_ladybug.png", "name": "瓢蟲"},
    {"img": "./assets/insect_ant.png", "name": "螞蟻"},
    {"img": "./assets/insect_bee.png", "name": "蜜蜂"},
    {"img": "./assets/insect_beetle.png", "name": "甲蟲"},
    {"img": "./assets/insect_cockroach.png", "name": "蟑螂"},
    {"img": "./assets/insect_spider.png", "name": "蜘蛛"},
    {"img": "./assets/insect_spiderweb.png", "name": "蜘蛛網"},
    {"img": "./assets/insect_scorpion.png", "name": "蠍子"},
    {"img": "./assets/insect_mosquito.png", "name": "蚊子"}
]
data_out["insects"] = ai_insects + data_out.get("insects", [])

# Note: Shapes, Numbers, Letters can be handled manually or dynamically
js_content = f"// 自動生成的真實相片庫 (包含 AI 插畫)\nconst gameData = {json.dumps(data_out, ensure_ascii=False, indent=2)};\n"
with open('data_auto.js', 'w', encoding='utf-8') as f:
    f.write(js_content)

print(f"Finished! Successfully collected {success_count} real photos.")
