Simple Campus Energy Dashboard (Robust Version)
Project Overview

This project is a Python-based dashboard and reporting system for campus energy consumption. It consolidates energy data from multiple building CSV files, handles missing or corrupt data safely, and produces both visual and textual summaries.

Key Features:

Reads multiple CSV files from a data/ folder.

Handles missing or corrupt timestamps and energy readings (kWh).

Generates cleaned and aggregated datasets.

Creates a comprehensive dashboard with daily, weekly, and scatter visualizations.

Exports:

cleaned_energy_data.csv – cleaned, combined data.

building_summary.csv – per-building summary statistics.

summary.txt – textual summary with key insights.

dashboard.png – visual representation of energy usage trends.

Folder Structure
CampusEnergyDashboard/
│
├─ data/                   # Place all building CSV files here
│    ├─ building1.csv
│    ├─ building2.csv
│    └─ ...
├─ main.py                 # Main Python script
├─ cleaned_energy_data.csv # Generated cleaned data
├─ building_summary.csv    # Generated building summary
├─ summary.txt             # Generated text summary
├─ dashboard.png           # Generated plots
└─ README.md

CSV File Requirements

Each CSV file should represent a building and must contain:

Column	Type	Notes
timestamp	datetime	ISO format (e.g., 2025-12-04 10:00)
kwh	numeric	Energy usage in kWh

Example:

timestamp,kwh
2025-12-01 00:00,5.2
2025-12-01 01:00,4.8
2025-12-01 02:00,5.0


The script automatically adds a building column using the CSV filename.

How to Run

Install dependencies (if not installed):

pip install pandas matplotlib


Place CSV files in the data/ folder.

Run the dashboard script:

python main.py


Output files generated:

cleaned_energy_data.csv – combined, cleaned data

building_summary.csv – summary statistics per building

summary.txt – text summary with total consumption, peak load, and top building

dashboard.png – visual dashboard

Dashboard Details

Daily Energy Consumption – line plot showing each building's daily usage.

Weekly Average Usage – bar chart of weekly average per building.

Peak Hour Consumption – scatter plot of energy readings over time.

Notes

If any CSV files are missing or malformed, the script will skip them with warnings.

Ensure your CSVs have timestamped energy readings for accurate analysis.

Inspect the highest-consuming buildings to optimize campus energy use.

Example Output
Total Campus Consumption: 1250.50 kWh
Highest Consuming Building: building3
Peak Load Time: 2025-12-02 15:00:00


Dashboard saved as dashboard.png.
