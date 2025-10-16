# NYC Mobility App

## Overview
This application provides data analysis and insights for NYC taxi trip data. The backend API serves trip data and analytical insights for over 1.45 million taxi trips.

## Features
- Database storage of 1.45+ million NYC taxi trips
- RESTful API with endpoints for raw data and analytical insights
- Data processing and cleaning pipeline
- Statistical analysis of trip patterns

## Project Structure
```
nyc_mobility_app/
├── app.py                          # Main Flask application entry point
├── README.md                       # Project documentation
├── SETUP_GUIDE.md                  # Detailed setup and connection guide
├── requirements.txt                # Python dependencies
├── backend/                        # Backend application code
│   ├── config/
│   │   └── db_config.py           # Database configuration
│   ├── data/
│   │   ├── cleaned/               # Processed data files
│   │   ├── logs/                  # Processing logs
│   │   └── raw/                   # Original data files
│   ├── models/
│   │   └── schema.sql             # Database schema definition
│   ├── routes/
│   │   ├── trips_routes.py        # API endpoints for trip data
│   │   └── insights_routes.py     # API endpoints for analytics
│   ├── scripts/
│   │   ├── data_cleaning.py       # Data cleaning pipeline
│   │   ├── feature_engineering.py # Feature creation scripts
│   │   └── insert_data.py         # Database population script
│   └── utils/
│       ├── db_connection.py       # Database connection utilities
│       ├── helpers.py             # Helper functions
│       └── custom_algorithm.py    # Custom analytics algorithms
├── frontend/                       # Frontend dashboard
│   ├── index.html                 # Main HTML page
│   └── static/                    # Static assets
│       ├── css/
│       │   └── styles.css         # Dashboard styling
│       └── js/
│           └── main.js            # Frontend JavaScript (API calls)
└── database/
    └── init_db.sql                # Database initialization script
```

## API Endpoints

### Frontend Routes
- `GET /` - Serves the main dashboard (index.html)
- `GET /static/css/styles.css` - Dashboard CSS
- `GET /static/js/main.js` - Dashboard JavaScript

### Backend API Routes
- `GET /api/trips/` - Access trip data with optional filtering
  - Query parameters: `limit`, `offset`, `min_speed`, `max_speed`
  - Example: `/api/trips/?limit=20&offset=0`
- `GET /api/trips/<trip_id>` - Get specific trip by ID
- `GET /api/insights/stats` - Get trip statistics (total trips, avg duration, avg speed, etc.)
- `GET /api/insights/hourly-pattern` - Get trip counts by hour of day

## Setup Instructions

### Prerequisites
- Python 3.x
- MySQL 8.0+
- pip

### Installation

1. Clone the repository:
```
git clone https://github.com/your-username/nyc_mobility_app.git
cd nyc_mobility_app
```

2. Create and activate a virtual environment:
```
python -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```
pip install -r requirements.txt
```

4. Setup the database:
```
 # Create database and user (run as MySQL root)
mysql -u root -p < database/init_db.sql
```
5. Configure the database connection:
  Edit backend/config/db_config.py with your MYSQL credentials:
```
MYSQL_HOST = "localhost"
MYSQL_USER = "kellia"       # Use the username you created
MYSQL_PASSWORD = "pass123"  # Use the password you created
MYSQL_DB = "nyc_mobility"   # This should match the database name
```
6. Create the database tables
```

# Create tables (run as your MySQL user)
mysql -u 'your_username' -p nyc_mobility < backend/models/schema.sql
```

5. Data insertion:
```
cd backend
python scripts/insert_data.py
```
Note: Data insertion may take time as it processes 1.45+ million records.

6. Start the application:
```
python3 app.py
```
7. Access the API at http://localhost:5000

## Frontend & Static Files

The frontend dashboard is served from `frontend/index.html` and uses static assets located in `frontend/static/`:
- CSS: `/static/css/styles.css`
- JavaScript: `/static/js/main.js`

Flask is configured to serve static files from the `frontend/static` directory. Make sure your HTML references these files as `/static/css/styles.css` and `/static/js/main.js`.

## How to Run

1. Start the backend server:
    ```
    python app.py
    ```
2. Open your browser and go to:
    ```
    http://localhost:5000
    ```
   The dashboard will load and connect to the backend API endpoints automatically.

3. API endpoints for data:
    - `GET /api/insights/stats` for statistics
    - `GET /api/trips/` for trip data

## Troubleshooting
- If you see 404 errors for static files, ensure your CSS and JS are in `frontend/static/css` and `frontend/static/js`.
- If you see CORS errors, ensure `flask-cors` is installed and `CORS(app)` is called in `app.py`.
- For database errors, check your MySQL configuration in `backend/config/db_config.py`.


## Video Walkthrough link
 - Find it here: https://youtu.be/JUBmoTxLdy8

## Contributors
- Kellia Kamikazi
- Aurore Umumararungu
- Rolande Tumugane
