import re
import sys
from bs4 import BeautifulSoup
import requests

url = "http://fifalive.click/"

# Pydroid 3 এবং রিয়েল মোবাইল ব্রাউজারের মতো নিখুঁত হেডার্স
headers = {
    "Host": "fifalive.click",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Linux; Android 14; 22071219AI Build/UP1A.231005.007) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.7827.163 Mobile Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "X-Requested-With": "mark.via.gp",
    "Referer": "http://fifalive.click/",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
}

try:
    # সেশন ব্যবহার করে কুকি হ্যান্ডেল করা, যাতে বট ডিটেক্ট না করতে পারে
    session = requests.Session()
    res = session.get(url, headers=headers, timeout=20)

    if res.status_code == 200:
        soup = BeautifulSoup(res.text, "html.parser")
        buttons = soup.select(".server-box .server-btn")

        if buttons:
            m3u_content = "#EXTM3U\n"
            links_found = False

            for btn in buttons:
                server_name = btn.text.strip()
                onclick_text = btn.get("onclick", "")
                match = re.search(r"changeServer\('([^']+)'", onclick_text)

                if match:
                    stream_link = match.group(1)
                    m3u_content += f'#EXTINF:-1 tvg-id="{server_name}" tvg-name="{server_name}" group-title="FIFA Sports", {server_name}\n'
                    m3u_content += f"{stream_link}\n"
                    links_found = True

            if links_found:
                with open("fifa.m3u", "w", encoding="utf-8") as f:
                    f.write(m3u_content)
                print("✅ Successfully updated fifa.m3u with new links.")
            else:
                print("❌ Buttons found, but no links extracted.")
                sys.exit(1)  # গিটহাব অ্যাকশনকে ফেইল দেখাবে যাতে আপনি বুঝতে পারেন
        else:
            print("❌ HTML-এ কোনো সার্ভার বাটন খুঁজে পাওয়া যায়নি! গিটহাবের আইপি ব্লক হতে পারে।")
            # পেজে কী লেখা আসছে তা চেক করার জন্য প্রিন্ট (লগ দেখার জন্য)
            print("--- HTML Response Snippet ---")
            print(res.text[:1000])
            sys.exit(1)
    else:
        print(f"❌ Failed to fetch website. Status Code: {res.status_code}")
        sys.exit(1)

except Exception as e:
    print(f"❌ Error occurred: {e}")
    sys.exit(1)
