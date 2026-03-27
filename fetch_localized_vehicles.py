import asyncio
import os
import urllib.request
from duckduckgo_search import AsyncDDGS

async def download_image(url, filename):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            with open(filename, 'wb') as f:
                f.write(response.read())
            print(f"Downloaded: {filename}")
            return True
    except Exception as e:
        print(f"Failed {url}: {e}")
    return False

async def fetch_specific_vehicles():
    search_map = {
        "計程車": "Taiwan yellow taxi toyota car realistic",
        "垃圾車": "Taiwan yellow garbage truck realistic",
        "吉普車": "Jeep Wrangler silver or yellow realistic",
        "水泥攪拌車": "Cement mixer truck realistic construction"
    }
    
    os.makedirs("assets", exist_ok=True)
    
    async with AsyncDDGS() as ddgs:
        for name, query in search_map.items():
            print(f"Searching for: {query}")
            try:
                # 使用 DuckDuckGo 搜尋高品質真實圖片
                results = await ddgs.images(query, max_results=5)
                success = False
                for r in results:
                    url = r['image']
                    # 簡單判斷副檔名
                    ext = ".jpg"
                    if ".png" in url.lower(): ext = ".png"
                    filename = f"assets/tw_vehicle_{name}{ext}"
                    
                    if await download_image(url, filename):
                        success = True
                        break
                if not success:
                    print(f"Could not find image for {name}")
            except Exception as e:
                print(f"Search error for {name}: {e}")

if __name__ == "__main__":
    asyncio.run(fetch_specific_vehicles())
