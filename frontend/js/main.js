const BACKEND_URL = 'http://127.0.0.1:5000/api/'; 

// 1. Function to fetch and display analytical insights
async function fetchInsights() {
    const container = document.getElementById('insights-container');
    container.innerHTML = 'Fetching insights...'; 

    try {
        const response = await fetch(BACKEND_URL + 'insights');
        const insights = await response.json(); 

        // ASSUMPTION: Backend returns an object with avg_fare and top_location
        container.innerHTML = `
            <div class="insight-card">
                <h3>Average Trip Fare:</h3>
                <p>$${insights.avg_fare ? insights.avg_fare.toFixed(2) : 'N/A'}</p>
            </div>
            <div class="insight-card">
                <h3>Top Pickup Location:</h3>
                <p>${insights.top_location || 'N/A'}</p>
            </div>
        `;

    } catch (error) {
        console.error('Error fetching insights:', error);
        container.innerHTML = '<p class="error">Failed to load insights. Ensure the backend is running.</p>';
    }
}


// 2. Function to fetch and display trip records
async function fetchTripData() {
    const tableBody = document.querySelector('#trips-table tbody');
    tableBody.innerHTML = ''; // Clear the initial 'Loading...' row

    try {
        const response = await fetch(BACKEND_URL + 'trips');
        const trips = await response.json(); 

        if (trips.length === 0) {
            tableBody.innerHTML = '<tr><td colspan="5">No trip data found.</td></tr>';
            return;
        }

        // Loop through the array of trips and create a table row for each
        trips.forEach(trip => {
            const row = tableBody.insertRow();
            
            // NOTE: Replace these property names (e.g., 'id', 'pickup_datetime') 
            // with the exact column names your backend API is sending!
            row.insertCell().textContent = trip.id || 'N/A';
            row.insertCell().textContent = trip.pickup_datetime ? new Date(trip.pickup_datetime).toLocaleString() : 'N/A';
            row.insertCell().textContent = trip.dropoff_datetime ? new Date(trip.dropoff_datetime).toLocaleString() : 'N/A';
            row.insertCell().textContent = trip.trip_distance ? trip.trip_distance.toFixed(2) : 'N/A';
            row.insertCell().textContent = trip.fare_amount ? '$' + trip.fare_amount.toFixed(2) : 'N/A';
        });

    } catch (error) {
        console.error('Error fetching trip data:', error);
        tableBody.innerHTML = '<tr><td colspan="5" class="error">Failed to load trip data. Ensure the backend is running.</td></tr>';
    }
}


// 3. Run the functions when the page loads
document.addEventListener('DOMContentLoaded', () => {
    fetchInsights();
    fetchTripData();
});
