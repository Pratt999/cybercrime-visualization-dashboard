import pandas as pd
import matplotlib.pyplot as plt

INPUT_FILE = "data/processed_data/cases_final_clean.csv"

df = pd.read_csv(INPUT_FILE)
df["date"] = pd.to_datetime(df["date"], errors="coerce")

# ---------- GRAPH 1: TIMELINE ----------
fig1, ax1 = plt.subplots()
timeline = df.groupby("date").size()
timeline.plot(ax=ax1)
ax1.set_title("Cyber Crime Incidents Over Time")
ax1.set_xlabel("Date")
ax1.set_ylabel("Number of Incidents")
ax1.grid(True)
plt.tight_layout()
plt.show()

# ---------- GRAPH 2: SEVERITY DISTRIBUTION ----------
fig2, ax2 = plt.subplots()
severity_timeline = (
    df.groupby(["date", "severity_level"])
    .size()
    .unstack(fill_value=0)
)
severity_timeline.plot(kind="bar", stacked=True, ax=ax2)
ax2.set_title("Severity Distribution Over Time")
ax2.set_xlabel("Date")
ax2.set_ylabel("Number of Incidents")
plt.tight_layout()
plt.show()

# ---------- GRAPH 3: REGIONAL DISTRIBUTION ----------
fig3, ax3 = plt.subplots()
region_counts = df.groupby("region").size()
region_counts.plot(kind="bar", ax=ax3)
ax3.set_title("Regional Distribution of Cyber Incidents")
ax3.set_xlabel("Region")
ax3.set_ylabel("Number of Incidents")
plt.tight_layout()
plt.show()
