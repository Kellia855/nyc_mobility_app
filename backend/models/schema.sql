-- Drop existing tables if they exist
DROP TABLE IF EXISTS trips;

-- Create trips table
CREATE TABLE IF NOT EXISTS trips (
    id VARCHAR(255) PRIMARY KEY,
    vendor_id VARCHAR(50),
    pickup_datetime DATETIME,
    dropoff_datetime DATETIME,
    passenger_count INT,
    pickup_longitude DOUBLE,
    pickup_latitude DOUBLE,
    dropoff_longitude DOUBLE,
    dropoff_latitude DOUBLE,
    store_and_fwd_flag VARCHAR(10),
    trip_duration INT,
    trip_distance_km DOUBLE,
    trip_duration_min DOUBLE,
    speed_kmh DOUBLE,
    fare_per_km DOUBLE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- Create indexes for improved query performance
CREATE INDEX idx_pickup_datetime ON trips (pickup_datetime);
CREATE INDEX idx_dropoff_datetime ON trips (dropoff_datetime);
CREATE INDEX idx_passenger_count ON trips (passenger_count);
CREATE INDEX idx_speed_kmh ON trips (speed_kmh);
