import pandas as pd
import csv

INPUT_FILE = "data/processed_data/cases_final.csv"
OUTPUT_FILE = "data/processed_data/cases_final_clean.csv"

# Read using maximum tolerance
df = pd.read_csv(
    INPUT_FILE,
    engine="python",
    sep=",",
    on_bad_lines="skip"
)

# Re-write with strict quoting
df.to_csv(
    OUTPUT_FILE,
    index=False,
    quoting=csv.QUOTE_ALL
)

print(f"Repaired CSV written to {OUTPUT_FILE}")
print(f"Rows kept: {len(df)}")
