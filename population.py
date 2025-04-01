#!/usr/bin/env python3
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
    <script src="https://cdn.jsdelivr.net/npm/apexcharts"></script>
    <style>
        body { padding: 20px; background-color: #f8f9fa; }
        .viz-card { margin-bottom: 20px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); border-radius: 8px; }
        .card-header { background-color: #0d6efd; color: white; font-weight: bold; }
        .chart-container { position: relative; height: 300px; width: 100%; }
        .progress { height: 25px; margin-bottom: 10px; }
        .flag { font-size: 1.8em; }
        .gauge { text-align: center; padding: 15px; }
        .gauge-value { font-size: 2rem; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container-fluid">
        <h1 class="text-center mb-4">🌍 Advanced Population Dashboard</h1>
        
        <!-- Row 1 -->
        <div class="row">
            <!-- Vis 1: Population Bar Chart -->
            <div class="col-lg-6">
                <div class="viz-card card">
                    <div class="card-header">1. Population by Country (Millions)</div>
                    <div class="card-body">
                        <canvas id="populationChart"></canvas>
                    </div>
                </div>
            </div>
            
            <!-- Vis 2: Growth Radar Chart -->
            <div class="col-lg-6">
                <div class="viz-card card">
                    <div class="card-header">2. Growth Rate Comparison</div>
                    <div class="card-body">
                        <canvas id="growthChart"></canvas>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Row 2 -->
        <div class="row">
            <!-- Vis 3: Population Pie Chart -->
            <div class="col-lg-6">
                <div class="viz-card card">
                    <div class="card-header">3. Population Distribution</div>
                    <div class="card-body">
                        <canvas id="pieChart"></canvas>
                    </div>
                </div>
            </div>
            
            <!-- Vis 4: Urbanization Bars -->
            <div class="col-lg-6">
                <div class="viz-card card">
                    <div class="card-header">4. Urban Population (%)</div>
                    <div class="card-body" id="urbanBars"></div>
                </div>
            </div>
        </div>
        
        <!-- Row 3 -->
        <div class="row">
            <!-- Vis 5: Density Scatter Plot -->
            <div class="col-lg-6">
                <div class="viz-card card">
                    <div class="card-header">5. Population Density (People/km²)</div>
                    <div class="card-body">
                        <canvas id="densityChart"></canvas>
                    </div>
                </div>
            </div>
            
            <!-- Vis 6: Fertility Gauges -->
            <div class="col-lg-6">
                <div class="viz-card card">
                    <div class="card-header">6. Fertility Rate (Children per Woman)</div>
                    <div class="card-body row" id="fertilityGauges"></div>
                </div>
            </div>
        </div>
        
        <!-- Vis 7: Data Table -->
        <div class="viz-card card">
            <div class="card-header">7. Complete Country Data</div>
            <div class="card-body">
                <table class="table table-striped table-hover">
                    <thead>
                        <tr>
                            <th>Flag</th>
                            <th>Country</th>
                            <th>Population (M)</th>
                            <th>Growth (%)</th>
                            <th>Density</th>
                            <th>Urban (%)</th>
                            <th>Fertility</th>
                        </tr>
                    </thead>
                    <tbody id="dataTable"></tbody>
                </table>
            </div>
        </div>
    </div>

    <script>
    document.addEventListener('DOMContentLoaded', function() {
        fetch('/data')
            .then(res => res.json())
            .then(data => {
                const colors = [
                    '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0',
                    '#9966FF', '#FF9F40', '#8AC24A'
                ];
                
                // 1. Population Bar Chart
                new Chart(document.getElementById('populationChart'), {
                    type: 'bar',
                    data: {
                        labels: data.map(d => d.name),
                        datasets: [{
                            label: 'Population (Millions)',
                            data: data.map(d => d.population),
                            backgroundColor: colors,
                            borderWidth: 1
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false
                    }
                });
                
                // 2. Growth Radar Chart
                new Chart(document.getElementById('growthChart'), {
                    type: 'radar',
                    data: {
                        labels: data.map(d => d.name),
                        datasets: [{
                            label: 'Growth Rate (%)',
                            data: data.map(d => d.growth),
                            backgroundColor: 'rgba(54, 162, 235, 0.2)',
                            borderColor: 'rgba(54, 162, 235, 1)',
                            pointBackgroundColor: 'rgba(54, 162, 235, 1)'
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false
                    }
                });
                
                // 3. Population Pie Chart
                new Chart(document.getElementById('pieChart'), {
                    type: 'pie',
                    data: {
                        labels: data.map(d => d.name),
                        datasets: [{
                            data: data.map(d => d.population),
                            backgroundColor: colors,
                            borderWidth: 1
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false
                    }
                });
                
                // 4. Urbanization Progress Bars
                let urbanHTML = '';
                data.forEach((country, index) => {
                    urbanHTML += `
                    <div>
                        <div class="d-flex justify-content-between mb-1">
                            <span>${country.flag} ${country.name}</span>
                            <span>${country.urban}%</span>
                        </div>
                        <div class="progress">
                            <div class="progress-bar" 
                                 style="width: ${country.urban}%; background-color: ${colors[index]}">
                            </div>
                        </div>
                    </div>`;
                });
                document.getElementById('urbanBars').innerHTML = urbanHTML;
                
                // 5. Density Scatter Plot
                new Chart(document.getElementById('densityChart'), {
                    type: 'scatter',
                    data: {
                        datasets: [{
                            label: 'Population Density',
                            data: data.map((d, i) => ({
                                x: d.population,
                                y: d.density,
                                r: d.growth * 5
                            })),
                            backgroundColor: colors,
                            borderWidth: 1
                        }]
                    },
                    options: {
                        scales: {
                            x: {
                                title: { display: true, text: 'Population (Millions)' }
                            },
                            y: {
                                title: { display: true, text: 'Density (People/km²)' }
                            }
                        }
                    }
                });
                
                // 6. Fertility Gauges
                let fertilityHTML = '';
                data.forEach((country, index) => {
                    fertilityHTML += `
                    <div class="col-md-4 gauge">
                        <div class="card">
                            <div class="card-body">
                                <div class="flag">${country.flag}</div>
                                <h5>${country.name}</h5>
                                <div class="gauge-value" style="color: ${colors[index]}">
                                    ${country.fertility}
                                </div>
                                <small>children/woman</small>
                            </div>
                        </div>
                    </div>`;
                });
                document.getElementById('fertilityGauges').innerHTML = fertilityHTML;
                
                // 7. Data Table
                let tableHTML = '';
                data.forEach(country => {
                    tableHTML += `
                    <tr>
                        <td>${country.flag}</td>
                        <td>${country.name}</td>
                        <td>${country.population.toLocaleString()}</td>
                        <td>${country.growth}</td>
                        <td>${country.density}</td>
                        <td>${country.urban}</td>
                        <td>${country.fertility}</td>
                    </tr>`;
                });
                document.getElementById('dataTable').innerHTML = tableHTML;
            });
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
