-- Initialize the NYC Mobility Database
-- Create database if it doesn't exist
CREATE DATABASE IF NOT EXISTS nyc_mobility;

-- Create user if it doesn't exist
CREATE USER IF NOT EXISTS 'kellia'@'localhost' IDENTIFIED BY 'pass123';

-- Grant privileges to the user on the database
GRANT ALL PRIVILEGES ON nyc_mobility.* TO 'kellia'@'localhost';

-- Apply the privileges
FLUSH PRIVILEGES;
-- Create database if it doesn't exist
CREATE DATABASE IF NOT EXISTS nyc_mobility;

-- Use the database
USE nyc_mobility;

-- Print success message
SELECT 'Database nyc_mobility created successfully!' AS 'Status';
