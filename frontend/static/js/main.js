const BACKEND_URL = 'http://127.0.0.1:5000/api'; 

// 1. Function to fetch and display analytical insights
async function fetchInsights() {
    const container = document.getElementById('insights-container');
    container.innerHTML = 'Fetching insights...'; 

    try {
        const response = await fetch(`${BACKEND_URL}/insights/stats`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const insights = await response.json(); 

        // Display the insights returned from /api/insights/stats
        container.innerHTML = `
            <div class="insight-card">
                <h3>Total Trips:</h3>
                <p>${insights.total_trips || 'N/A'}</p>
            </div>
            <div class="insight-card">
                <h3>Average Duration:</h3>
                <p>${insights.avg_duration_min ? insights.avg_duration_min.toFixed(2) + ' min' : 'N/A'}</p>
            </div>
            <div class="insight-card">
                <h3>Average Speed:</h3>
                <p>${insights.avg_speed_kmh ? insights.avg_speed_kmh.toFixed(2) + ' km/h' : 'N/A'}</p>
            </div>
            <div class="insight-card">
                <h3>Average Distance:</h3>
                <p>${insights.avg_distance_km ? insights.avg_distance_km.toFixed(2) + ' km' : 'N/A'}</p>
            </div>
        `;

    } catch (error) {
        console.error('Error fetching insights:', error);
        container.innerHTML = '<p class="error">Failed to load insights. Ensure the backend is running.</p>';
    }
}


// 2. Function to fetch and display trip records
async function fetchTripData(minSpeed = 0, maxSpeed = null) {
    const tableBody = document.querySelector('#trips-table tbody');
    tableBody.innerHTML = '<tr><td colspan="5">Loading...</td></tr>';

    try {
        let url = `${BACKEND_URL}/trips/?limit=20&min_speed=${minSpeed}`;
        if (maxSpeed) {
            url += `&max_speed=${maxSpeed}`;
        }
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        const trips = data.trips || [];

        tableBody.innerHTML = '';

        if (trips.length === 0) {
            tableBody.innerHTML = '<tr><td colspan="5">No trip data found.</td></tr>';
            return;
        }

        trips.forEach(trip => {
            const row = tableBody.insertRow();
            row.insertCell().textContent = trip.trip_id || 'N/A';
            row.insertCell().textContent = trip.pickup_datetime ? new Date(trip.pickup_datetime).toLocaleString() : 'N/A';
            row.insertCell().textContent = trip.dropoff_datetime ? new Date(trip.dropoff_datetime).toLocaleString() : 'N/A';
            row.insertCell().textContent = trip.trip_distance_km ? trip.trip_distance_km.toFixed(2) : 'N/A';
            row.insertCell().textContent = trip.fare_amount ? '$' + trip.fare_amount.toFixed(2) : 'N/A';
        });

    } catch (error) {
        console.error('Error fetching trip data:', error);
        tableBody.innerHTML = '<tr><td colspan="5" class="error">Failed to load trip data. Ensure the backend is running.</td></tr>';
    }
}


// 3. Run the functions when the page loads

// 4. Add filter button event for fare
document.addEventListener('DOMContentLoaded', () => {
    fetchInsights();
    fetchTripData();
    fetchHourlyPattern();

    const filterBtn = document.getElementById('filter-btn');
    if (filterBtn) {
        filterBtn.addEventListener('click', () => {
            const minSpeed = document.getElementById('min-speed').value || 0;
            const maxSpeed = document.getElementById('max-speed').value || null;
            fetchTripData(minSpeed, maxSpeed);
        });
    }

    fetchPassengerDistribution();
});

// 5. Visualization: Trips per Hour (Chart.js)
async function fetchHourlyPattern() {
    const chartElem = document.getElementById('hourlyChart');
    if (!chartElem) return;
    try {
        const response = await fetch(`${BACKEND_URL}/insights/hourly-pattern`);
        if (!response.ok) throw new Error('Failed to fetch hourly pattern');
        const data = await response.json();
        
        // Find peak hours
        const maxCount = Math.max(...data.counts);
        const peakHours = data.hours.filter((h, i) => data.counts[i] === maxCount);
        const minCount = Math.min(...data.counts);
        const lowHours = data.hours.filter((h, i) => data.counts[i] === minCount);
        
        // Display insight text
        const insightElem = document.getElementById('hourly-insight');
        if (insightElem) {
            insightElem.innerHTML = `<strong>Insight:</strong> Peak taxi demand occurs at hour ${peakHours.join(', ')} (${maxCount.toLocaleString()} trips). 
            Lowest demand is at hour ${lowHours.join(', ')} (${minCount.toLocaleString()} trips). 
            This pattern suggests strong commuter usage during evening hours.`;
        }
        
        new Chart(chartElem, {
            type: 'bar',
            data: {
                labels: data.hours,
                datasets: [{
                    label: 'Trips per Hour',
                    data: data.counts,
                    backgroundColor: 'rgba(54, 162, 235, 0.6)'
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: { display: false },
                    title: { display: true, text: 'NYC Trips per Hour' }
                },
                scales: {
                    x: { title: { display: true, text: 'Hour of Day' } },
                    y: { title: { display: true, text: 'Number of Trips' } }
                }
            }
        });
    } catch (err) {
        console.error('Error loading hourly pattern:', err);
    }
}

// 6. Visualization: Passenger Distribution (Pie Chart)
async function fetchPassengerDistribution() {
    const chartElem = document.getElementById('passengerChart');
    if (!chartElem) return;
    try {
        const response = await fetch(`${BACKEND_URL}/insights/passenger-distribution`);
        if (!response.ok) throw new Error('Failed to fetch passenger distribution');
        const data = await response.json();
        
        // Calculate total and percentages
        const total = data.counts.reduce((sum, count) => sum + count, 0);
        const maxCount = Math.max(...data.counts);
        const maxIndex = data.counts.indexOf(maxCount);
        const mostCommon = data.labels[maxIndex];
        const percentage = ((maxCount / total) * 100).toFixed(1);
        
        // Display insight text
        const insightElem = document.getElementById('passenger-insight');
        if (insightElem) {
            insightElem.innerHTML = `<strong>Insight:</strong> Most trips (${percentage}%) are taken by ${mostCommon.toLowerCase()}. 
            This indicates that NYC taxis primarily serve individual commuters rather than groups.`;
        }
        
        new Chart(chartElem, {
            type: 'pie',
            data: {
                labels: data.labels,
                datasets: [{
                    data: data.counts,
                    backgroundColor: [
                        'rgba(255, 99, 132, 0.7)',
                        'rgba(54, 162, 235, 0.7)',
                        'rgba(255, 206, 86, 0.7)',
                        'rgba(75, 192, 192, 0.7)',
                        'rgba(153, 102, 255, 0.7)',
                        'rgba(255, 159, 64, 0.7)'
                    ]
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: { position: 'right' },
                    title: { display: true, text: 'Trip Distribution by Passenger Count' }
                }
            }
        });
    } catch (err) {
        console.error('Error loading passenger distribution:', err);
    }
}

