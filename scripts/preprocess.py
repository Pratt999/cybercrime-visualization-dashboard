import json
import pandas as pd
from email.utils import parsedate_to_datetime

INPUT_FILE = "data/raw_data/incidents.json"
OUTPUT_FILE = "data/processed_data/cases.csv"

def infer_attack_type(title, description):
    text = (title + " " + description).lower()

    if "ransomware" in text:
        return "Ransomware"
    if "phishing" in text:
        return "Phishing"
    if "ddos" in text:
        return "DDoS"
    if "malware" in text:
        return "Malware"
    if "breach" in text or "vulnerability" in text:
        return "Data Breach"
    return "Unknown"

def preprocess():
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        incidents = json.load(f)

    records = []

    for idx, item in enumerate(incidents, start=1):
        raw_date = item.get("published_date", "")

        try:
            parsed_date = parsedate_to_datetime(raw_date).date()
        except Exception:
            parsed_date = None

        record = {
            "case_id": f"CC{idx:03}",
            "date": parsed_date,
            "country": "Unknown",
            "region": "Global",
            "attack_type": infer_attack_type(
                item.get("title", ""),
                item.get("description", "")
            ),
            "sector": "Industrial / Critical Infrastructure",
            "description": item.get("title", ""),
            "legal_action": "Under Investigation",
            "source": item.get("source", "CISA")
        }

        records.append(record)

    df = pd.DataFrame(records)
    df.to_csv(OUTPUT_FILE, index=False)

    print(f"Processed {len(df)} cases into {OUTPUT_FILE}")

if __name__ == "__main__":
    preprocess()
