
🌦️ Weather Data Visualizer – Mini Project

Course: Programming for Problem Solving using Python
Student: Kunal Yadav
Repository Name: weather-data-visualizer-<yourname>

📌 Project Overview

This mini-project analyses real-world weather data using Python.
It demonstrates data loading, cleaning, processing, statistical calculations, grouping, and visualization.
The project helps understand climate patterns using Pandas, NumPy, and Matplotlib.

🎯 Learning Outcomes

By completing this project, I practiced:

Loading and inspecting real CSV weather datasets

Cleaning missing values and converting datatypes

Performing daily/monthly/yearly statistical analysis

Visualizing trends using Matplotlib

Grouping data to find seasonal or monthly insights

Exporting cleaned data, plots, and summary reports

Writing modular, well-commented Python code

📂 Project Structure
weather-data-visualizer-<yourname>/
│
├── full_analysis.py               # Main Python script (combined code)
├── weather_data_raw.csv           # Original dataset (downloaded or sample)
├── weather_data_cleaned.csv       # Cleaned CSV after preprocessing
│
├── plots/                         # All generated PNG plots
│   ├── temperature_trend.png
│   ├── monthly_rainfall.png
│   ├── humidity_vs_temp.png
│   └── combined_figure.png
│
├── summary_report.md              # Insights + storytelling explanation
└── README.md                      # (This file)

📊 Tasks Performed
Task 1 – Data Acquisition & Loading

Downloaded a real weather dataset (Kaggle/IMD/open-source).

Loaded it using pandas.read_csv().

Inspected structure using .head(), .info(), .describe().

Task 2 – Data Cleaning

Removed/filled missing values.

Converted Date to datetime.

Filtered relevant columns: temperature, humidity, rainfall.

Task 3 – Statistical Analysis

Using NumPy and Pandas:

Mean, Min, Max, Standard deviation

Daily & monthly averages

Seasonal summaries

Task 4 – Visualizations

Created using Matplotlib:
✔ Daily temperature line chart
✔ Monthly rainfall bar chart
✔ Humidity vs temperature scatter plot
✔ Combined figure with subplots
All charts saved as PNG files.

Task 5 – Grouping & Aggregation

Grouped data by month using df.groupby(df['Date'].dt.month)

Calculated total rainfall, average temperature, humidity ranges

Also demonstrated seasonal grouping

Task 6 – Export & Storytelling

Saved cleaned dataset as CSV

Exported all plots

Generated summary_report.md describing:

Trends

Anomalies

Interpretations

Why climate awareness matters

📈 Example Outputs

Rising/falling temperature trends

Total rainfall per month

Relationship between humidity & temperature

Seasonal averages for better climate understanding

▶️ How to Run the Project
Step 1: Install Dependencies
pip install pandas numpy matplotlib

Step 2: Run the Python Script
python full_analysis.py

Step 3: Check Output Files

Cleaned data → weather_data_cleaned.csv

Plots → inside the plots/ folder

Summary → summary_report.md
