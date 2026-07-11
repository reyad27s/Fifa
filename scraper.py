import re
from bs4 import BeautifulSoup
import requests

url = "http://fifalive.click/"
headers = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 14) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Mobile Safari/537.36"
}

try:
    res = requests.get(url, headers=headers, timeout=15)
    if res.status_code == 200:
        soup = BeautifulSoup(res.text, "html.parser")
        buttons = soup.select(".server-box .server-btn")

        if buttons:
            # M3U ফাইলের হেডার তৈরি
            m3u_content = "#EXTM3U\n"

            for btn in buttons:
                server_name = btn.text.strip()
                onclick_text = btn.get("onclick", "")
                match = re.search(r"changeServer\('([^']+)'", onclick_text)

                if match:
                    stream_link = match.group(1)
                    # M3U ফরম্যাটে চ্যানেল অ্যাড করা
                    m3u_content += f'#EXTINF:-1 tvg-id="{server_name}" tvg-name="{server_name}" group-title="FIFA Sports", {server_name}\n'
                    m3u_content += f"{stream_link}\n"

            # fifa.m3u নামে ফাইলটি রাইট করা
            with open("fifa.m3u", "w", encoding="utf-8") as f:
                f.write(m3u_content)
            print("Successfully created/updated fifa.m3u")
        else:
            print("No servers found.")
    else:
        print(f"Failed to fetch website. Status: {res.status_code}")
except Exception as e:
    print(f"Error: {e}")
