import pandas as pd

INPUT_FILE = "data/processed_data/cases_with_mitre.csv"
OUTPUT_FILE = "data/processed_data/cases_final.csv"

def calculate_cia_and_severity(row):
    conf = 0
    integ = 0
    avail = 0
    score = 0

    attack_type = str(row["attack_type"]).lower()
    impact = str(row["mitre_impact"]).lower()

    # Confidentiality
    if "phishing" in attack_type or "credential" in impact or "exfiltration" in impact:
        conf = 1
        score += 3

    # Integrity
    if "malware" in attack_type or "unauthorized" in impact or "integrity" in impact:
        integ = 1
        score += 2

    # Availability
    if "ransomware" in attack_type or "ddos" in attack_type or "service" in impact:
        avail = 1
        score += 3

    # Vulnerability exploitation
    if "exploitation" in row["mitre_initial_access"].lower():
        integ = 1
        avail = 1
        score += 2

    # Severity level
    if score <= 2:
        level = "Low"
    elif score <= 5:
        level = "Medium"
    elif score <= 8:
        level = "High"
    else:
        level = "Critical"

    return pd.Series([
        conf, integ, avail, score, level
    ])

def apply_severity_scoring():
    df = pd.read_csv(INPUT_FILE)

    df[[
        "confidentiality_impact",
        "integrity_impact",
        "availability_impact",
        "severity_score",
        "severity_level"
    ]] = df.apply(calculate_cia_and_severity, axis=1)

    df.to_csv(OUTPUT_FILE, index=False)
    print(f"Severity scoring applied → {OUTPUT_FILE}")

if __name__ == "__main__":
    apply_severity_scoring()
