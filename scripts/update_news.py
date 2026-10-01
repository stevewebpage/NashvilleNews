import json
import os
import sys
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone

FEED_URL = os.environ.get("FEED_URL", "https://feeds.npr.org/1002/rss.xml")
SOURCE = "NPR"
HOW_MANY = 4

req = urllib.request.Request(FEED_URL, headers={"User-Agent": "NashvilleNews-bot"})
with urllib.request.urlopen(req, timeout=30) as resp:
    xml_data = resp.read()

root = ET.fromstring(xml_data)
stories = []
for item in root.iter("item"):
    title = (item.findtext("title") or "").strip()
    link = (item.findtext("link") or "").strip()
    if title and link:
        stories.append({"title": title, "link": link})
    if len(stories) == HOW_MANY:
        break

if not stories:
    print("No stories found - leaving news.json as it is.")
    sys.exit(1)

out = {
    "source": SOURCE,
    "updated": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
    "stories": stories,
}
with open("news.json", "w", encoding="utf-8") as f:
    json.dump(out, f, indent=2, ensure_ascii=False)
print("Saved", len(stories), "stories.")
