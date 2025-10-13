import pandas as pd
import mysql.connector
from mysql.connector import Error
import os
import numpy as np
import sys

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.db_config import get_db_config

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FEATURED_FILE = os.path.join(BASE_DIR, "data/cleaned/featured_trips.csv")

def insert_trips():
    print(f"Loading data from {FEATURED_FILE}")
    
    # Load CSV
    df = pd.read_csv(FEATURED_FILE)
    print(f"Loaded {len(df)} rows from CSV")
    
    # Properly handle NaN values - this is the key fix
    df = df.replace({np.nan: None})
    
    # Ensure string columns are proper strings, but leave None values as None
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].apply(lambda x: str(x) if x is not None else None)

    # Ensure 'id' is string if your table uses VARCHAR
    df['id'] = df['id'].astype(str)

    try:
        # Get database config
        db_config = get_db_config()
        
        # Connect to MySQL server (without specifying database initially)
        conn = mysql.connector.connect(
            host=db_config['host'],
            user=db_config['user'],
            password=db_config['password']
        )
        if conn.is_connected():
            print("Connected to MySQL server")

        cursor = conn.cursor()
        
        # Create database if it doesn't exist
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_config['database']}")
        cursor.execute(f"USE {db_config['database']}")
        print(f"Using database {db_config['database']}")
        
        # Create table if it doesn't exist
        create_table_query = """
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
        )
        """
        cursor.execute(create_table_query)
        print("Table 'trips' is ready")

        # Insert query
        insert_query = """
        INSERT INTO trips (
            id, vendor_id, pickup_datetime, dropoff_datetime, passenger_count,
            pickup_longitude, pickup_latitude, dropoff_longitude, dropoff_latitude,
            store_and_fwd_flag, trip_duration, trip_distance_km, trip_duration_min,
            speed_kmh, fare_per_km
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        success_count = 0
        error_count = 0
        
        # First try a small batch to verify the fix
        test_rows = 10
        print(f"Testing with first {test_rows} rows...")
        
        for i, (_, row) in enumerate(df.head(test_rows).iterrows()):
            # Convert row to list of values - this correctly handles None values
            values = [row[col] for col in df.columns]
            
            try:
                cursor.execute(insert_query, values)
                success_count += 1
                print(f"Test row {i+1} inserted successfully")
            except Error as e:
                error_count += 1
                print(f"Error with test row {i+1}: {e}")
                
        # Commit the test batch
        conn.commit()
        print(f"Test batch: {success_count} rows inserted, {error_count} errors")
        
        # If test is successful, proceed with batched inserts for the rest
        if success_count == test_rows:
            print("Test successful! Processing remaining data in batches...")
            
            batch_size = 1000
            total_rows = len(df)
            batch_count = 0
            
            # Start from where we left off
            for i in range(test_rows, total_rows, batch_size):
                end_idx = min(i + batch_size, total_rows)
                batch_count += 1
                print(f"Processing batch {batch_count}: rows {i+1}-{end_idx} of {total_rows}")
                
                batch_values = []
                for _, row in df.iloc[i:end_idx].iterrows():
                    row_values = [row[col] for col in df.columns]
                    batch_values.append(tuple(row_values))
                
                try:
                    cursor.executemany(insert_query, batch_values)
                    conn.commit()
                    success_count += len(batch_values)
                    print(f"Batch {batch_count} inserted successfully")
                except Error as e:
                    print(f"Error with batch {batch_count}: {e}")
                    print("Trying row by row...")
                    
                    # If batch fails, try one by one
                    for j, values in enumerate(batch_values):
                        try:
                            cursor.execute(insert_query, values)
                            conn.commit()
                            success_count += 1
                        except Error as e2:
                            error_count += 1
                            if error_count < 20:  # Limit error reporting
                                print(f"Error at row {i+j+1}: {e2}")
                
                # Report progress
                if batch_count % 10 == 0:
                    print(f"Progress: {min(i + batch_size, total_rows)}/{total_rows} rows processed")
        
        # Final commit and report
        conn.commit()
        print(f"Final results: {success_count} rows inserted successfully, {error_count} rows with errors.")

    except Error as e:
        print("Error while connecting to MySQL:", e)

    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
            print("MySQL connection closed.")

if __name__ == "__main__":
    insert_trips()

