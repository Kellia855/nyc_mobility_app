import pandas as pd
import os
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Paths
CLEANED_FILE = os.path.join(BASE_DIR, "data/cleaned/cleaned_trips.csv")
FEATURED_DIR = os.path.join(BASE_DIR, "data/cleaned/")
FEATURED_FILE = os.path.join(FEATURED_DIR, "featured_trips.csv")
LOG_FILE = os.path.join(BASE_DIR, "data/logs/excluded_records.log")

# Create log directory if it doesn't exist
os.makedirs(os.path.join(BASE_DIR, "data/logs/"), exist_ok=True)

# Load cleaned data
df = pd.read_csv(CLEANED_FILE)

# Open log file
log = open(LOG_FILE, "a")

#  Derived features
# Trip duration in minutes (if not already)
if "trip_duration_min" not in df.columns:
    # coerce to numeric first so missing/invalid values become NaN (not Python None)
    df["trip_duration_min"] = pd.to_numeric(df["trip_duration"], errors="coerce") / 60

# Speed in km/h
if "speed_kmh" not in df.columns:
    # Ensure numeric types and avoid division by zero or None
    df["trip_distance_km"] = pd.to_numeric(df["trip_distance_km"], errors="coerce")
    duration_hours = pd.to_numeric(df["trip_duration_min"], errors="coerce") / 60
    # replace zero durations with NaN to avoid inf values
    duration_hours = duration_hours.replace(0, np.nan)
    df["speed_kmh"] = df["trip_distance_km"] / duration_hours

# Fare per km (if fare_amount column exists)
if "fare_amount" in df.columns:
    # coerce to numeric so invalid values become NaN instead of Python None
    df["fare_per_km"] = pd.to_numeric(df["fare_amount"], errors="coerce") / pd.to_numeric(df["trip_distance_km"], errors="coerce")
else:
    # use np.nan for missing numeric columns so comparisons like <= 0 work safely
    df["fare_per_km"] = np.nan
# Remove unrealistic values
invalid_rows = pd.DataFrame()

if "speed_kmh" in df.columns:
    invalid_speed = df[(df["speed_kmh"] <= 0) | (df["speed_kmh"] > 150)]
    if not invalid_speed.empty:
        log.write("=== Removed rows with unrealistic speeds ===\n")
        log.write(invalid_speed.to_string(index=False) + "\n\n")
        invalid_rows = pd.concat([invalid_rows, invalid_speed])

if "fare_per_km" in df.columns:
    invalid_fare = df[df["fare_per_km"] <= 0]
    if not invalid_fare.empty:
        log.write("=== Removed rows with invalid fare/km ===\n")
        log.write(invalid_fare.to_string(index=False) + "\n\n")
        invalid_rows = pd.concat([invalid_rows, invalid_fare])

# Drop invalid rows
df = df.drop(index=invalid_rows.index)

# Save featured data
df.to_csv(FEATURED_FILE, index=False)
log.close()

print(f"Feature engineering done. Featured file saved to {FEATURED_FILE}")
print(f"Excluded rows are logged in {LOG_FILE}")

