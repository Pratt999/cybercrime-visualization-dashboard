import requests
import xml.etree.ElementTree as ET
import json
from datetime import datetime, timezone
import os

RSS_URL = "https://www.cisa.gov/cybersecurity-advisories/all.xml"
OUTPUT_DIR = "data/raw_data"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "incidents.json")

def fetch_cisa_alerts():
    response = requests.get(RSS_URL)
    response.raise_for_status()

    root = ET.fromstring(response.content)
    incidents = []

    for item in root.findall(".//item")[:30]:
        title = item.find("title").text
        description = item.find("description").text
        pub_date = item.find("pubDate").text
        link = item.find("link").text

        incidents.append({
            "title": title,
            "description": description,
            "published_date": pub_date,
            "source": "CISA",
            "link": link,
            "fetched_at": datetime.now(timezone.utc).isoformat()
        })

    return incidents

if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    data = fetch_cisa_alerts()
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

    print(f"Saved {len(data)} incidents to {OUTPUT_FILE}")
