import os
import urllib.request
import time

def download_image(url, filename):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})
        with urllib.request.urlopen(req, timeout=15) as response:
            with open(filename, 'wb') as f:
                f.write(response.read())
            print(f"Downloaded: {filename}")
            return True
    except Exception as e:
        print(f"Failed {url}: {e}")
    return False

def main():
    os.makedirs("assets", exist_ok=True)
    
    targets = {
        "計程車": "https://upload.wikimedia.org/wikipedia/commons/e/ea/Toyota_Wish_of_Taiwan_Taxi_Corp_TAA-610_20150807.jpg",
        "垃圾車": "https://upload.wikimedia.org/wikipedia/commons/6/69/Taipei_City_Waste_Collection_Truck_20120129.jpg",
        "吉普車": "https://upload.wikimedia.org/wikipedia/commons/e/ef/Jeep_Wrangler_TJ.jpg",
        "水泥攪拌車": "https://upload.wikimedia.org/wikipedia/commons/d/d4/Concrete_Transport_Truck.jpg"
    }
    
    for name, url in targets.items():
        filename = f"assets/tw_vehicle_{name}.jpg"
        print(f"Downloading {name}...")
        if download_image(url, filename):
            time.sleep(5) # 休息五秒

if __name__ == "__main__":
    main()
