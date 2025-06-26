# ML Monitoring Pipeline with Evidently + PostgreSQL + Docker

This project implements a containerized machine learning monitoring system using:

- **Evidently**: for metric calculation and HTML dashboards
- **PostgreSQL**: for storing metrics (quantile values)
- **Docker Compose**: to orchestrate all services

## 📦 Project Structure

monitoring/
│
├── data/
│ └── yellow_tripdata_2024-03.parquet # NYC taxi data
│
├── dashboards/
│ ├── fare_amount_median.html # Static single report
│ └── daily_YYYY-MM-DD.html # Per-day monitoring reports
│
├── generate_report.py # One-off report and insert
├── monitor.py # Batch daily monitoring loop
├── requirements.txt # Python dependencies
├── Dockerfile # Evidently container
└── docker-compose.yml # Compose file for all services


