import os
import json
import time
import urllib.request
import urllib.parse
from urllib.error import HTTPError
try:
    from duckduckgo_search import DDGS
except ImportError:
    print("Please pip install -U duckduckgo-search then run me.")
    exit(1)

import ssl
ssl._create_default_https_context = ssl._create_unverified_context

items = {
    "animals": [
        "獅子", "老虎", "豹", "雪豹", "美洲獅", "獵豹", "斑馬", "大猩猩", "紅毛猩猩", "犀牛",
        "河馬", "長頸鹿", "水牛", "駱駝", "羊駝", "貓熊", "無尾熊", "袋鼠", "狐狸", "野狼",
        "貓咪", "狗狗", "小豬", "猴子", "狒狒", "黑猩猩", "浣熊", "白馬", "棕馬", "小白兔",
        "野兔", "老鼠", "倉鼠", "天竺鼠", "松鼠", "刺蝟", "蝙蝠", "乳牛", "鹿", "麋鹿",
        "綿羊", "山羊", "企鵝", "北極熊", "海豹", "海龜", "鯊魚", "鯨魚", "海豚", "水獺"
    ],
    "vehicles": [
        "汽車", "計程車", "休旅車", "跑車", "吉普車", "電動車", "公車", "遊覽車", "娃娃車", "垃圾車",
        "郵務車", "警用汽車", "救護車", "消防車", "大貨車", "貨櫃車", "拖吊車", "拖拉機", "堆高機", "挖土機",
        "推土機", "水泥車", "砂石車", "重機", "野狼機車", "腳踏車", "電動自行車", "滑板車", "滑板", "蒸汽火車",
        "高鐵", "火車", "捷運", "輕軌電車", "直升機", "小飛機", "客機", "戰鬥機", "太空梭", "太空火箭",
        "獨木舟", "帆船", "快艇", "水上摩托車", "橡皮艇", "豪華郵輪", "渡輪", "潛水艇", "熱氣球", "纜車"
    ],
    "household": [
        "沙發", "茶几", "木頭椅子", "餐椅", "餐桌", "書桌", "雙人床", "嬰兒床", "衣櫃", "鞋櫃",
        "大門", "全身鏡", "玻璃窗", "電風扇", "吹風機", "冷氣機", "除濕機", "洗衣機", "冰箱", "微波爐",
        "烤箱", "瓦斯爐", "抽油煙機", "熱水瓶", "電鍋", "洗碗機", "馬桶", "浴缸", "蓮蓬頭", "肥皂",
        "洗髮乳", "牙刷", "牙膏", "毛巾", "掃把", "拖把", "垃圾桶", "鬧鐘", "液晶電視", "智慧型手機",
        "筆記型電腦", "桌上型電腦", "印表機", "電源插座", "鎢絲燈泡", "手電筒", "鐵鎚", "活動扳手", "螺絲起子", "滅火器"
    ],
    "fruits": [
        "蘋果", "香蕉", "橘子", "柳丁", "葡萄", "草莓", "櫻桃", "藍莓", "芒果", "鳳梨",
        "西瓜", "哈密瓜", "木瓜", "水蜜桃", "奇異果", "檸檬", "酪梨", "芭樂", "百香果", "蓮霧",
        "火龍果", "柿子", "柚子", "釋迦", "番茄", "高麗菜", "大白菜", "青江菜", "空心菜", "菠菜",
        "花椰菜", "綠花椰菜", "胡蘿蔔", "白蘿蔔", "馬鈴薯", "地瓜", "芋頭", "洋蔥", "大蒜", "青蔥",
        "芹菜", "蘆筍", "玉米", "小黃瓜", "大黃瓜", "南瓜", "苦瓜", "冬瓜", "茄子", "青椒"
    ],
    "insects": [
        "蒼蠅", "果蠅", "小黑蚊", "蟋蟀", "蚱蜢", "蚯蚓", "螳螂", "夏蟬", "蜻蜓", "螢火蟲",
        "蜈蚣", "馬陸", "蜘蛛", "蠍子", "毛毛蟲", "蠶寶寶", "大白斑蝶", "鳳蝶", "飛蛾", "蝸牛",
        "蛞蝓", "瓢蟲", "螞蟻", "紅火蟻", "白蟻", "蜜蜂", "虎頭蜂", "獨角仙", "鍬形蟲", "金龜子"
    ],
    "dinosaurs": [
        "暴龍", "腕龍", "劍龍", "三角龍", "翼龍", "迅猛龍", "副櫛龍", "甲龍", "棘龍", "雷龍",
        "厚頭龍", "蛇頸龍", "魚龍", "滄龍", "竊蛋龍", "慈母龍", "異特龍", "圓角龍", "重爪龍", "梁龍"
    ]
}

os.makedirs('assets', exist_ok=True)
data_out = {}
fail_count = 0
success_count = 0

with DDGS() as ddgs:
    for category, name_list in items.items():
        data_out[category] = []
        for name in name_list:
            # Check if we already have the AI generated perfectly rendered version
            ai_path = ""
            if category == "dinosaurs" and name in ["暴龍", "腕龍", "劍龍", "三角龍", "翼龍"]:
                ai_path = f"dino_{name}.png".replace("暴龍","trex").replace("腕龍","brachiosaurus").replace("劍龍","stegosaurus").replace("三角龍","triceratops").replace("翼龍","pteranodon")
                if os.path.exists(os.path.join('assets', ai_path)):
                    data_out[category].append({"img": f"./assets/{ai_path}", "name": name})
                    continue
            
            ai_insect_names = {"毛毛蟲":"caterpillar", "蝴蝶":"butterfly", "蝸牛":"snail", "瓢蟲":"ladybug", "螞蟻":"ant", "蜜蜂":"bee", "甲蟲":"beetle", "蟑螂":"cockroach", "蜘蛛":"spider", "蜘蛛網":"spiderweb", "蠍子":"scorpion", "蚊子":"mosquito"}
            if category == "insects" and name in ai_insect_names:
                ai_path = f"insect_{ai_insect_names[name]}.png"
                if os.path.exists(os.path.join('assets', ai_path)):
                    data_out[category].append({"img": f"./assets/{ai_path}", "name": name})
                    continue

            # Force DDG to return Photo type instead of Vector Graphics
            query = f"{name} 實體 相片 攝影"
            if category == "dinosaurs":
                query = f"{name} 模型 寫實"

            safe_name = f"z_{category}_{name}.jpg"
            img_path = os.path.join('assets', safe_name)
            
            # Skip downloading if already exists
            if os.path.exists(img_path) and os.path.getsize(img_path) > 1024:
                data_out[category].append({"img": f"./assets/{safe_name}", "name": name})
                print(f"Skipped {safe_name} (already exists)")
                continue
                
            print(f"[{category}] 正在抓取: {name} ...", end="", flush=True)
            try:
                # type_image="photo" guarantees no icons!
                results = list(ddgs.images(query, max_results=2, type_image="photo"))
                if not results:
                    print(f" 無結果")
                    continue
                
                img_url = results[0]["image"]
                # In case duckduckgo serves a broken URL or wiki icon, check extension
                if ".svg" in img_url.lower():
                    if len(results) > 1: img_url = results[1]["image"]
                    else:
                        print(" 只有 SVG")
                        continue
                
                req = urllib.request.Request(img_url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req, timeout=5) as response, open(img_path, 'wb') as out_file:
                    out_file.write(response.read())
                    
                data_out[category].append({"img": f"./assets/{safe_name}", "name": name})
                success_count += 1
                print(" OK!")
            except Exception as e:
                print(f" Error: {e}")
                fail_count += 1
                
            time.sleep(1) # Crucial: prevent IP rate-limiting from DDG !

js_content = f"// DDG 自動生成的最高畫質相片庫\nconst newData = {json.dumps(data_out, ensure_ascii=False, indent=2)};\n"
with open('data_ddg.js', 'w', encoding='utf-8') as f:
    f.write(js_content)

print(f"\\n--- DOWLOAD FINISHED ---\\nSuccess: {success_count}, Failed: {fail_count}")
