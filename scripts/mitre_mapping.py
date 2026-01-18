import pandas as pd

INPUT_FILE = "data/processed_data/cases.csv"
OUTPUT_FILE = "data/processed_data/cases_with_mitre.csv"

def map_mitre_tactics(attack_type, description):
    attack_type = str(attack_type).lower()
    description = str(description).lower()

    initial_access = "Unknown"
    execution = "Unknown"
    impact = "Unknown"

    if attack_type == "phishing":
        initial_access = "Phishing"
        execution = "User Execution"
        impact = "Credential Access"

    elif attack_type == "malware":
        initial_access = "Drive-by Compromise"
        execution = "Malicious File"
        impact = "Command and Control"

    elif attack_type == "ransomware":
        initial_access = "Phishing"
        execution = "Payload Execution"
        impact = "Data Encrypted for Impact"

    elif attack_type == "ddos":
        initial_access = "External Remote Services"
        execution = "Network Flooding"
        impact = "Service Disruption"

    elif attack_type == "data breach":
        initial_access = "Exploitation of Public-Facing Application"
        execution = "Credential Access"
        impact = "Exfiltration"

    else:
        # Vulnerability advisories / exploited components
        if "vulnerability" in description or "exploited" in description:
            initial_access = "Exploitation of Vulnerability"
            execution = "Unauthorized Code Execution"
            impact = "Integrity Violation"

    return initial_access, execution, impact

def apply_mitre_mapping():
    df = pd.read_csv(INPUT_FILE)

    mitre_data = df.apply(
        lambda row: map_mitre_tactics(
            row["attack_type"],
            row["description"]
        ),
        axis=1,
        result_type="expand"
    )

    mitre_data.columns = [
        "mitre_initial_access",
        "mitre_execution",
        "mitre_impact"
    ]

    df = pd.concat([df, mitre_data], axis=1)
    df.to_csv(OUTPUT_FILE, index=False)

    print(f"MITRE ATT&CK mapping applied → {OUTPUT_FILE}")

if __name__ == "__main__":
    apply_mitre_mapping()
