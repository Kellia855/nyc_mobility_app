"""
Helper functions for the NYC mobility app
"""
import datetime
import math

def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the great-circle distance between two points on Earth
    given their latitude and longitude in decimal degrees.
    Returns distance in kilometers.
    """
    # Convert decimal degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    r = 6371  # Radius of Earth in kilometers
    return c * r

def parse_datetime(datetime_str):
    """
    Parse datetime string to datetime object
    """
    try:
        return datetime.datetime.fromisoformat(datetime_str.replace('Z', '+00:00'))
    except ValueError:
        try:
            return datetime.datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            try:
                return datetime.datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M:%S')
            except ValueError:
                raise ValueError(f"Could not parse datetime string: {datetime_str}")

def calculate_trip_duration_minutes(start_time, end_time):
    """
    Calculate trip duration in minutes between two datetime objects
    """
    if isinstance(start_time, str):
        start_time = parse_datetime(start_time)
    
    if isinstance(end_time, str):
        end_time = parse_datetime(end_time)
    
    duration = end_time - start_time
    return duration.total_seconds() / 60
