import os
import pandas as pd
import psycopg2
from evidently.report import Report
from evidently.metrics import ColumnQuantileMetric
from datetime import datetime

#Load the data
df = pd.read_parquet("data/yellow_tripdata_2024-03.parquet")
df["pickup_datetime"] = pd.to_datetime(df["pickup_datetime"])

# Reference = 1st March
ref_date = pd.Timestamp("2024-03-01")
ref_data = df[df["pickup_datetime"].dt.date == ref_date.date()]

# Looping through easch date in March 2024
for day in range(2, 32):
    day_str = f"2024-03-{day:02d}"
    print(f"\n📊 Processing {day_str}...")
    curr_data = df[df["pickup_datetime"].dt.date == pd.Timestamp(day_str).date()]

    if curr_data.empty:
        print(f"⚠️ No data for {day_str}, skipping...")
        continue

    report = Report(metrics=[
        ColumnQuantileMetric(column_name="fare_amount", quantile=0.5)
    ])
    report.run(reference_data=ref_data, current_data=curr_data)

    # Save HTML
    report_path = f"dashboards/daily_{day_str}.html"
    report.save_html(report_path)

    # Extract metric
    report_dict = report.as_dict()
    metric_result = report_dict['metrics'][0].get('result', {})
    metric_value = metric_result.get('current', {}).get('value')

    if metric_value is not None:
        try:
            conn = psycopg2.connect(
                host="postgres",
                port=5432,
                user="root",
                password="root",
                dbname="monitoring"
            )
            cur = conn.cursor()

            cur.execute("""
                CREATE TABLE IF NOT EXISTS quantile_metrics (
                    date DATE,
                    metric_name TEXT,
                    value FLOAT
                );
            """)

            cur.execute(
                "INSERT INTO quantile_metrics (date, metric_name, value) VALUES (%s, %s, %s);",
                (day_str, "fare_amount_0.5", metric_value)
            )

            conn.commit()
            cur.close()
            conn.close()

            print(f"✅ Inserted {metric_value} for {day_str}")
        except Exception as e:
            print(f"❌ DB insert failed for {day_str}: {e}")
    else:
        print(f"⚠️ Metric missing for {day_str}, skipped.")
