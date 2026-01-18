from flask import Flask, render_template
import pandas as pd
import plotly.express as px

app = Flask(__name__)

DATA_FILE = "../data/processed_data/cases_final_clean.csv"

@app.route("/")
def index():
    df = pd.read_csv(DATA_FILE)
    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    # Timeline
    timeline = df.groupby("date").size().reset_index(name="count")
    fig_timeline = px.line(
        timeline,
        x="date",
        y="count",
        title="Cyber Crime Incidents Over Time"
    )

    # Severity Distribution
    severity = (
        df.groupby(["date", "severity_level"])
        .size()
        .reset_index(name="count")
    )
    fig_severity = px.bar(
        severity,
        x="date",
        y="count",
        color="severity_level",
        title="Severity Distribution Over Time",
        barmode="stack"
    )

    # Regional Distribution
    region = df.groupby("region").size().reset_index(name="count")
    fig_region = px.bar(
        region,
        x="region",
        y="count",
        title="Regional Distribution of Cyber Incidents"
    )

    return render_template(
        "index.html",
        timeline=fig_timeline.to_html(full_html=False),
        severity=fig_severity.to_html(full_html=False),
        region=fig_region.to_html(full_html=False)
    )

if __name__ == "__main__":
    app.run(debug=True)
