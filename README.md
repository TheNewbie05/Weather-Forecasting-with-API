# 🌤️ End-to-End Weather Analytics Pipeline

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Power BI](https://img.shields.io/badge/Power_BI-Dashboard-yellow.svg)](https://powerbi.microsoft.com/)
[![SQLite](https://img.shields.io/badge/SQLite-Database-green.svg)](https://www.sqlite.org/index.html)

A comprehensive data engineering project that automates the collection of real-time weather data for 15+ Indian cities, stores it in a relational database, and visualizes 1-year historical trends using Power BI.

## 🚀 Key Features
- **Automated ETL:** Python scripts to fetch, clean, and transform live weather data from OpenWeatherMap API.
- **Data Persistence:** Robust SQLite/MySQL database schema for storing time-series weather logs.
- **Advanced Simulation:** Custom script to generate 365 days of realistic seasonal data for trend analysis.
- **Power BI Dashboard:** Interactive visuals featuring heatmaps, seasonal correlations, and peak-hour analysis.

## 🏗️ Project Architecture
1. **Extraction:** Fetching JSON data via REST API.
2. **Transformation:** Data cleaning, unit conversion (Kelvin to Celsius), and timestamp normalization using Pandas.
3. **Loading:** Bulk ingestion into RDBMS.
4. **Visualization:** Connecting Power BI to the DB and building a Star Schema model.

## 📁 Project Structure

```text
.
├── database/               # SQLite/MySQL database and connection logic
├── docs/                   # Project documentation and PDF reports
├── src/                    # Core Python source code
│   ├── etl_pipeline.py     # Main Extract, Transform, Load logic
│   └── mock_generator.py   # 1-Year realistic data simulation script
├── .gitignore              # Files and folders to be ignored by Git
├── README.md               # Detailed project overview and setup guide
└── requirements.txt        # List of Python libraries (Pandas, Requests, etc.)

```
## 📊 Dashboard Insights
Seasonality Trends: Tracking temperature shifts from Summer to Winter across India.

Humidity vs. Rainfall: Correlation analysis using scatter plots and combo charts.

Extreme Weather Alerts: Identifying highest and lowest recorded temperatures per city.

Peak Hour Analysis: Understanding intraday temperature fluctuations.

## 🛠️ Tech Stack
Languages: Python, SQL, DAX

Libraries: Pandas, Requests, Sqlite3, Schedule

Tools: Power BI Desktop, VS Code, Git/GitHub

## ⚙️ Setup Instructions
Clone the repository:

Bash
git clone [https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git](https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git)
Install dependencies:

Bash
pip install -r requirements.txt
Run the ETL script:

## Bash
python src/etl_pipeline.py
Open the .pbix file in Power BI and refresh the data.

## 👨‍💻 Author
## Vishal Kumbhakar
