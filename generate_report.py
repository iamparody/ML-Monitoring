import pandas as pd
import json
import psycopg2
from evidently.report import Report
from evidently.metrics import ColumnQuantileMetric

df = pd.read_parquet("data/green_tripdata_2024-03.parquet")

report = Report(metrics=[ColumnQuantileMetric(column_name="fare_amount", quantile=0.5)])
report.run(reference_data=df, current_data=df)


report.run(reference_data=df, current_data=df)


report.save_html("dashboards/fare_amount_median.html")

# Save the report as JSON FOR INSPECTION
report_dict = report.as_dict()
with open("dashboards/metric_output.json", "w") as f:
    json.dump(report_dict, f, indent=2)

metric_result = report_dict['metrics'][0].get('result', {})
metric_value = metric_result.get('current', {}).get('value')


if metric_value is not None:
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
            metric_name TEXT,
            value FLOAT
        );
    """)

    cur.execute(
        "INSERT INTO quantile_metrics (metric_name, value) VALUES (%s, %s);",
        ("fare_amount_0.5", metric_value)
    )

    conn.commit()
    cur.close()
    conn.close()
    print(f" Inserted value: {metric_value}")
else:
    print("Metric value not found. Skipping insert.")