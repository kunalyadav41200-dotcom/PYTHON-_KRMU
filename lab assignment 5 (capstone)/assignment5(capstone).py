"""
Campus Energy-Use Dashboard - Full unified script
Single-file implementation combining all tasks (ingest, aggregate, OOP model,
visualization, persistence, and executive summary).

Usage:
 - Place building CSVs in ./data/ with columns: timestamp,kwh
 - Run: python campus_energy_dashboard_full.py
 - Outputs placed in ./output/

Author: Kunal Yadav
Date: 4-dec-2025
"""

import os
import sys
import logging
from pathlib import Path
from datetime import datetime

import pandas as pd
import matplotlib.pyplot as plt

# ------------------------- Configuration ---------------------------------
DATA_DIR = Path("data")
OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = OUTPUT_DIR / "ingest.log"

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s",
                    handlers=[
                        logging.FileHandler(LOG_FILE),
                        logging.StreamHandler(sys.stdout)
                    ])

# ------------------------- OOP Models -----------------------------------
class MeterReading:
    """Represents a single meter reading."""
    def __init__(self, timestamp: pd.Timestamp, kwh: float):
        self.timestamp = pd.Timestamp(timestamp)
        self.kwh = float(kwh)

    def to_dict(self, building_name: str):
        return {"building": building_name, "timestamp": self.timestamp, "kwh": self.kwh}


class Building:
    """Holds readings for a single building and offers simple analytics."""
    def __init__(self, name: str):
        self.name = name
        self.readings = []  # list of MeterReading

    def add_reading(self, reading: MeterReading):
        self.readings.append(reading)

    def to_dataframe(self) -> pd.DataFrame:
        if not self.readings:
            return pd.DataFrame(columns=["building", "timestamp", "kwh"]).set_index("timestamp")
        rows = [r.to_dict(self.name) for r in self.readings]
        df = pd.DataFrame(rows).set_index("timestamp")
        df.index = pd.to_datetime(df.index)
        return df

    def calculate_total_consumption(self) -> float:
        return sum(r.kwh for r in self.readings)

    def generate_report(self) -> dict:
        df = self.to_dataframe()
        if df.empty:
            return {"building": self.name, "total_kwh": 0, "mean_kwh": 0, "min_kwh": 0, "max_kwh": 0}
        total = df['kwh'].sum()
        return {
            "building": self.name,
            "total_kwh": total,
            "mean_kwh": float(df['kwh'].mean()),
            "min_kwh": float(df['kwh'].min()),
            "max_kwh": float(df['kwh'].max())
        }


class BuildingManager:
    """Manages multiple Building instances."""
    def __init__(self):
        self.buildings = {}

    def add_building(self, building: Building):
        self.buildings[building.name] = building

    def get_or_create(self, name: str) -> Building:
        if name not in self.buildings:
            self.buildings[name] = Building(name)
        return self.buildings[name]

    def combined_dataframe(self) -> pd.DataFrame:
        dfs = []
        for b in self.buildings.values():
            df = b.to_dataframe()
            if not df.empty:
                dfs.append(df.assign(building=b.name))
        if not dfs:
            return pd.DataFrame(columns=["building", "kwh"])  # empty
        combined = pd.concat(dfs)
        combined.index.name = "timestamp"
        combined.sort_index(inplace=True)
        return combined

    def generate_all_reports(self) -> pd.DataFrame:
        reports = [b.generate_report() for b in self.buildings.values()]
        return pd.DataFrame(reports)

# ------------------------- Data Ingestion --------------------------------

def ingest_data(data_dir: Path) -> BuildingManager:
    """Reads all CSV files from data_dir and populates BuildingManager.
    Expects CSVs with columns: timestamp,kwh (timestamp parseable by pandas)
    If building name is not present inside the CSV, it is inferred from filename.
    Corrupt rows are skipped.
    """
    bm = BuildingManager()
    if not data_dir.exists():
        logging.error(f"Data directory {data_dir} not found.")
        return bm

    csv_files = list(sorted(data_dir.glob("*.csv")))
    if not csv_files:
        logging.warning(f"No CSV files found in {data_dir}")
        return bm

    for csv_path in csv_files:
        building_name = csv_path.stem  # e.g., library.csv -> library
        logging.info(f"Reading {csv_path} for building '{building_name}'")
        try:
            # Use on_bad_lines='skip' to skip malformed rows (pandas >= 1.3)
            df = pd.read_csv(csv_path, parse_dates=['timestamp'], infer_datetime_format=True, on_bad_lines='skip')
        except TypeError:
            # fallback for older pandas versions
            df = pd.read_csv(csv_path, parse_dates=['timestamp'], infer_datetime_format=True, error_bad_lines=False)
        except FileNotFoundError:
            logging.exception(f"File not found: {csv_path}")
            continue
        except Exception:
            logging.exception(f"Failed to read {csv_path}. Skipping.")
            continue

        # Normalize column names
        df.columns = [c.strip().lower() for c in df.columns]
        if 'timestamp' not in df.columns or 'kwh' not in df.columns:
            logging.error(f"File {csv_path} missing required columns (timestamp, kwh). Skipping.")
            continue

        # Drop rows with NaN timestamp or kwh
        df = df.dropna(subset=['timestamp', 'kwh'])

        # Ensure numeric kwh
        df['kwh'] = pd.to_numeric(df['kwh'], errors='coerce')
        df = df.dropna(subset=['kwh'])

        # Convert timestamps to pandas Timestamp
        df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
        df = df.dropna(subset=['timestamp'])

        building = bm.get_or_create(building_name)
        for idx, row in df.iterrows():
            try:
                reading = MeterReading(row['timestamp'], row['kwh'])
                building.add_reading(reading)
            except Exception:
                logging.exception(f"Failed to add reading from row {idx} in {csv_path}")
                continue

        logging.info(f"Loaded {len(building.readings)} readings for {building_name}")
    return bm

# ------------------------- Aggregation Logic ------------------------------

def calculate_daily_totals(df: pd.DataFrame) -> pd.DataFrame:
    """Returns a DataFrame indexed by date with daily total kwh per building and a total column."""
    if df.empty:
        return pd.DataFrame()
    df = df.copy()
    df['date'] = df.index.floor('D')
    daily = df.groupby(['building', 'date'])['kwh'].sum().unstack(level=0).fillna(0)
    daily['campus_total'] = daily.sum(axis=1)
    return daily


def calculate_weekly_aggregates(df: pd.DataFrame) -> pd.DataFrame:
    """Returns weekly totals (week ending) per building."""
    if df.empty:
        return pd.DataFrame()
    weekly = df.copy()
    # Resample per building by weekly sum
    weekly_totals = []
    for b in df['building'].unique():
        bdf = df[df['building'] == b].resample('W')['kwh'].sum().rename(b)
        weekly_totals.append(bdf)
    if not weekly_totals:
        return pd.DataFrame()
    weekly_df = pd.concat(weekly_totals, axis=1).fillna(0)
    weekly_df['campus_total'] = weekly_df.sum(axis=1)
    return weekly_df


def building_wise_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Compute mean, min, max, total per building."""
    if df.empty:
        return pd.DataFrame()
    summary = df.groupby('building')['kwh'].agg(['mean', 'min', 'max', 'sum']).rename(columns={'sum': 'total'})
    summary = summary.reset_index()
    return summary

# ------------------------- Visualization ---------------------------------

def create_dashboard(df_combined: pd.DataFrame, daily_df: pd.DataFrame, weekly_df: pd.DataFrame, output_path: Path):
    """Creates a 3-chart dashboard and saves it to output_path."""
    if df_combined.empty:
        logging.warning("No data available for plotting.")
        return

    buildings = sorted(df_combined['building'].unique())
    plt.close('all')
    fig, axes = plt.subplots(3, 1, figsize=(12, 14), constrained_layout=True)

    # 1) Trend Line – daily consumption over time for all buildings
    ax = axes[0]
    if not daily_df.empty:
        for b in buildings:
            if b in daily_df.columns:
                ax.plot(daily_df.index, daily_df[b], label=b)
    ax.set_title('Daily Consumption Trend by Building')
    ax.set_xlabel('Date')
    ax.set_ylabel('kWh')
    ax.legend()

    # 2) Bar Chart – compare average weekly usage across buildings
    ax = axes[1]
    if not weekly_df.empty:
        avg_weekly = weekly_df.mean().drop('campus_total', errors='ignore')
        avg_weekly.sort_values(ascending=False, inplace=True)
        ax.bar(avg_weekly.index, avg_weekly.values)
        ax.set_title('Average Weekly Usage per Building')
        ax.set_xlabel('Building')
        ax.set_ylabel('Average Weekly kWh')
        ax.tick_params(axis='x', rotation=45)

    # 3) Scatter Plot – plot peak-hour consumption vs. time/building
    ax = axes[2]
    # Compute hourly maxima per building
    hourly = df_combined.copy()
    hourly = hourly[['kwh', 'building']]
    hourly = hourly.resample('H').agg({'kwh': 'sum', 'building': lambda s: ','.join(sorted(set(s)))})
    # For a meaningful scatter, compute per-reading peak points (we'll scatter per-reading)
    for b in buildings:
        bdf = df_combined[df_combined['building'] == b].resample('H')['kwh'].sum()
        if not bdf.empty:
            ax.scatter(bdf.index, bdf.values, label=b, s=10)
    ax.set_title('Hourly Consumption Scatter (per building)')
    ax.set_xlabel('Timestamp')
    ax.set_ylabel('kWh')
    ax.legend(markerscale=2, bbox_to_anchor=(1.02, 1), loc='upper left')

    plt.suptitle('Campus Energy-Use Dashboard', fontsize=16)
    plt.savefig(output_path, bbox_inches='tight')
    logging.info(f"Dashboard saved to {output_path}")

# ------------------------- Reporting & Persistence -----------------------

def export_cleaned_data(df_combined: pd.DataFrame, out_csv: Path):
    if df_combined.empty:
        logging.warning("No cleaned data to export.")
        return
    df_combined.to_csv(out_csv)
    logging.info(f"Cleaned data exported to {out_csv}")


def export_summary_csv(summary_df: pd.DataFrame, out_csv: Path):
    if summary_df.empty:
        logging.warning("No summary to export.")
        return
    summary_df.to_csv(out_csv, index=False)
    logging.info(f"Building summary exported to {out_csv}")


def write_text_summary(summary_df: pd.DataFrame, daily_df: pd.DataFrame, weekly_df: pd.DataFrame, out_txt: Path):
    lines = []
    total_campus = float(daily_df['campus_total'].sum()) if (not daily_df.empty and 'campus_total' in daily_df.columns) else 0
    lines.append(f"Total campus consumption (from daily totals): {total_campus:.2f} kWh")

    if not summary_df.empty:
        top = summary_df.sort_values('total', ascending=False).iloc[0]
        lines.append(f"Highest-consuming building: {top['building']} ({top['total']:.2f} kWh total)")
    else:
        lines.append("Highest-consuming building: N/A")

    # Peak load time - find timestamp of max campus hourly or daily
    if not weekly_df.empty:
        peak_week = weekly_df['campus_total'].idxmax()
        lines.append(f"Week with highest campus load (week-ending): {peak_week.date()}")

    if not daily_df.empty:
        peak_day = daily_df['campus_total'].idxmax()
        lines.append(f"Day with highest campus load: {peak_day.date()}")

    # Add simple trend notes
    if not weekly_df.empty:
        # compare mean weekday vs weekend roughly
        lines.append(f"Average weekly campus consumption: {weekly_df['campus_total'].mean():.2f} kWh")

    lines.append("\nObservations and suggestions:")
    lines.append("- Investigate highest-consuming buildings for HVAC or lighting optimization.")
    lines.append("- Target peak hours for demand-side management or load shifting.")

    out_txt.write_text('\n'.join(lines))
    logging.info(f"Text summary written to {out_txt}")

# ------------------------- Main Pipeline --------------------------------

def run_pipeline(data_dir: Path, output_dir: Path):
    bm = ingest_data(data_dir)
    df_combined = bm.combined_dataframe()

    # If empty, create a friendly message and exit gracefully
    if df_combined.empty:
        logging.error("No meter readings loaded. Exiting pipeline.")
        return

    # Ensure index is datetime and sorted
    if not isinstance(df_combined.index, pd.DatetimeIndex):
        df_combined.index = pd.to_datetime(df_combined.index)
    df_combined.sort_index(inplace=True)

    # Aggregations
    daily_df = calculate_daily_totals(df_combined)
    weekly_df = calculate_weekly_aggregates(df_combined)
    summary_df = building_wise_summary(df_combined)

    # Persistence
    cleaned_path = output_dir / 'cleaned_energy_data.csv'
    summary_csv_path = output_dir / 'building_summary.csv'
    dashboard_path = output_dir / 'dashboard.png'
    summary_txt_path = output_dir / 'summary.txt'

    export_cleaned_data(df_combined, cleaned_path)
    export_summary_csv(summary_df, summary_csv_path)

    # Visualization
    create_dashboard(df_combined, daily_df, weekly_df, dashboard_path)

    # Text summary
    write_text_summary(summary_df, daily_df, weekly_df, summary_txt_path)

    logging.info("Pipeline completed successfully.")


# ------------------------- CLI / Runner ---------------------------------
def main():
    print("Campus Energy-Use Dashboard - Unified Script")
    print("Reading CSVs from ./data/ and writing outputs to ./output/")
    run_pipeline(DATA_DIR, OUTPUT_DIR)


if __name__ == '__main__':
    main()
