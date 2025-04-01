from flask import Flask, jsonify
import os

app = Flask(__name__)

# Sample population data
countries = [
    {"name": "India", "population": 1428, "growth": 0.9, "density": 464, "urban": 35, "fertility": 2.1, "flag": "🇮🇳"},
    {"name": "China", "population": 1425, "growth": 0.4, "density": 153, "urban": 61, "fertility": 1.7, "flag": "🇨🇳"},
    {"name": "USA", "population": 339, "growth": 0.6, "density": 36, "urban": 83, "fertility": 1.8, "flag": "🇺🇸"},
    {"name": "Indonesia", "population": 277, "growth": 1.1, "density": 151, "urban": 57, "fertility": 2.2, "flag": "🇮🇩"},
    {"name": "Pakistan", "population": 240, "growth": 2.0, "density": 287, "urban": 37, "fertility": 3.5, "flag": "🇵🇰"},
    {"name": "Brazil", "population": 216, "growth": 0.7, "density": 25, "urban": 87, "fertility": 1.7, "flag": "🇧🇷"},
    {"name": "Nigeria", "population": 223, "growth": 2.6, "density": 226, "urban": 52, "fertility": 5.1, "flag": "🇳🇬"}
]

@app.route('/')
def dashboard():
    return """
<!DOCTYPE html>
<html>
<head>
    <title>Population Dashboard</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body { padding: 20px; }
        .chart-container { height: 300px; }
        .card { margin-bottom: 20px; }
    </style>
</head>
<body>
    <div class="container">
        <h1 class="text-center mb-4">🌍 Population Dashboard</h1>
        
        <div class="row">
            <div class="col-md-6">
                <div class="card">
                    <div class="card-header">Population by Country</div>
                    <div class="card-body">
                        <div class="chart-container">
                            <canvas id="populationChart"></canvas>
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-md-6">
                <div class="card">
                    <div class="card-header">Growth Rates</div>
                    <div class="card-body">
                        <div class="chart-container">
                            <canvas id="growthChart"></canvas>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="card mt-4">
            <div class="card-header">Country Data</div>
            <div class="card-body">
                <table class="table">
                    <thead>
                        <tr>
                            <th>Country</th>
                            <th>Population</th>
                            <th>Growth</th>
                        </tr>
                    </thead>
                    <tbody id="dataTable"></tbody>
                </table>
            </div>
        </div>
    </div>

    <script>
    fetch('/data')
        .then(res => res.json())
        .then(data => {
            // Population Chart
            new Chart(document.getElementById('populationChart'), {
                type: 'bar',
                data: {
                    labels: data.map(d => d.name),
                    datasets: [{
                        label: 'Population (millions)',
                        data: data.map(d => d.population),
                        backgroundColor: 'rgba(54, 162, 235, 0.7)'
                    }]
                }
            });
            
            // Growth Chart
            new Chart(document.getElementById('growthChart'), {
                type: 'line',
                data: {
                    labels: data.map(d => d.name),
                    datasets: [{
                        label: 'Growth (%)',
                        data: data.map(d => d.growth),
                        borderColor: 'rgba(255, 99, 132, 0.7)'
                    }]
                }
            });
            
            // Table Data
            let tableHTML = '';
            data.forEach(country => {
                tableHTML += `
                <tr>
                    <td>${country.flag} ${country.name}</td>
                    <td>${country.population}</td>
                    <td>${country.growth}%</td>
                </tr>`;
            });
            document.getElementById('dataTable').innerHTML = tableHTML;
        });
    </script>
</body>
</html>
    """

@app.route('/data')
def get_data():
    return jsonify(countries)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)