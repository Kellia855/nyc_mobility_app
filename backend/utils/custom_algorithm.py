"""
Custom algorithm implementation for NYC mobility insights
"""
import pandas as pd
import numpy as np
from .helpers import haversine_distance

def estimate_trip_fare(distance_km, duration_min, passenger_count=1):
    """
    Estimate a trip fare based on distance, duration, and passenger count
    
    This is a simple example algorithm - you would replace this with your actual
    custom algorithm logic.
    """
    # Base fare
    base_fare = 2.50
    
    # Distance component: $2.50 per km
    distance_fare = distance_km * 2.50
    
    # Time component: $0.50 per minute
    time_fare = duration_min * 0.50
    
    # Passenger surcharge: $0.50 per additional passenger beyond the first
    passenger_surcharge = max(0, passenger_count - 1) * 0.50
    
    # Total fare
    total_fare = base_fare + distance_fare + time_fare + passenger_surcharge
    
    return round(total_fare, 2)

def identify_peak_hours(trip_df):
    """
    Identify peak hours based on trip volume
    Returns a list of hour integers (0-23)
    """
    # Convert pickup_datetime to datetime if it's not already
    if trip_df['pickup_datetime'].dtype != 'datetime64[ns]':
        trip_df['pickup_datetime'] = pd.to_datetime(trip_df['pickup_datetime'])
    
    # Extract hour from pickup_datetime
    trip_df['hour'] = trip_df['pickup_datetime'].dt.hour
    
    # Count trips by hour
    hourly_counts = trip_df['hour'].value_counts().sort_index()
    
    # Calculate the mean and standard deviation of hourly counts
    mean_count = hourly_counts.mean()
    std_count = hourly_counts.std()
    
    # Identify hours that are more than 1 std dev above the mean
    peak_hours = hourly_counts[hourly_counts > (mean_count + std_count)].index.tolist()
    
    return peak_hours

def detect_outlier_speeds(speeds, z_threshold=3.0):
    """
    Detect outlier speeds using z-score method
    Returns boolean array where True indicates an outlier
    """
    z_scores = np.abs((speeds - np.mean(speeds)) / np.std(speeds))
    return z_scores > z_threshold
