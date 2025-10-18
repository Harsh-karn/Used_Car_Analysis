#!/usr/bin/env python3
"""
Used Cars Analysis - Minimal Flask API for Vercel
No external data files - uses mock data
"""

from flask import Flask, jsonify, request, send_file
import json
import os

app = Flask(__name__)

# Mock data for demonstration
MOCK_DATA = {
    'stats': {
        'total_cars': 1000,
        'average_price': 5.2,
        'price_range': {'min': 0.44, 'max': 160.0},
        'year_range': {'min': 1998, 'max': 2019},
        'unique_brands': 32,
        'most_common_fuel': 'Petrol',
        'most_common_transmission': 'Manual'
    },
    'brands': [
        {'brand': 'Maruti', 'average_price': 4.5, 'count': 250},
        {'brand': 'Hyundai', 'average_price': 5.8, 'count': 200},
        {'brand': 'Honda', 'average_price': 7.2, 'count': 150},
        {'brand': 'Toyota', 'average_price': 8.1, 'count': 120},
        {'brand': 'Ford', 'average_price': 6.5, 'count': 100},
        {'brand': 'BMW', 'average_price': 25.3, 'count': 50},
        {'brand': 'Mercedes', 'average_price': 28.7, 'count': 45},
        {'brand': 'Audi', 'average_price': 22.1, 'count': 40}
    ],
    'years': [
        {'year': 2019, 'count': 150, 'average_price': 6.8},
        {'year': 2018, 'count': 180, 'average_price': 6.2},
        {'year': 2017, 'count': 200, 'average_price': 5.8},
        {'year': 2016, 'count': 220, 'average_price': 5.1},
        {'year': 2015, 'count': 250, 'average_price': 4.8}
    ],
    'fuel': [
        {'fuel_type': 'Petrol', 'average_mileage': 18.5, 'count': 600, 'average_price': 5.8},
        {'fuel_type': 'Diesel', 'average_mileage': 22.1, 'count': 350, 'average_price': 6.2},
        {'fuel_type': 'CNG', 'average_mileage': 20.3, 'count': 50, 'average_price': 4.5}
    ],
    'transmission': [
        {'transmission': 'Manual', 'count': 700, 'average_price': 5.2},
        {'transmission': 'Automatic', 'count': 300, 'average_price': 8.7}
    ],
    'owner': [
        {'owner_type': 'First', 'count': 500, 'average_price': 6.8},
        {'owner_type': 'Second', 'count': 350, 'average_price': 4.2},
        {'owner_type': 'Third', 'count': 100, 'average_price': 3.1},
        {'owner_type': 'Fourth & Above', 'count': 50, 'average_price': 2.5}
    ],
    'engine': [
        {'engine_range': '0-1000', 'average_price': 3.2},
        {'engine_range': '1000-2000', 'average_price': 5.8},
        {'engine_range': '2000-3000', 'average_price': 8.5},
        {'engine_range': '3000-4000', 'average_price': 15.2},
        {'engine_range': '4000-5000', 'average_price': 25.8}
    ],
    'correlation': [
        {'feature': 'Power', 'correlation': 0.85},
        {'feature': 'Engine', 'correlation': 0.78},
        {'feature': 'Transmission', 'correlation': 0.65},
        {'feature': 'Year', 'correlation': 0.58},
        {'feature': 'Mileage', 'correlation': -0.42},
        {'feature': 'Owner_Type', 'correlation': -0.35}
    ]
}

@app.route('/')
def home():
    """Home page - serve index.html"""
    if os.path.exists('index.html'):
        return send_file('index.html')
    else:
        return jsonify({
            "message": "Used Cars Analysis API",
            "status": "Demo version with sample data",
            "endpoints": [
                "/api/stats",
                "/api/brands", 
                "/api/years",
                "/api/fuel",
                "/api/transmission",
                "/api/owner",
                "/api/engine",
                "/api/correlation",
                "/api/search"
            ]
        })

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get dataset statistics"""
    return jsonify(MOCK_DATA['stats'])

@app.route('/api/brands', methods=['GET'])
def get_brands():
    """Get brand analysis"""
    return jsonify(MOCK_DATA['brands'])

@app.route('/api/years', methods=['GET'])
def get_years():
    """Get year analysis"""
    return jsonify(MOCK_DATA['years'])

@app.route('/api/fuel', methods=['GET'])
def get_fuel():
    """Get fuel type analysis"""
    return jsonify(MOCK_DATA['fuel'])

@app.route('/api/transmission', methods=['GET'])
def get_transmission():
    """Get transmission analysis"""
    return jsonify(MOCK_DATA['transmission'])

@app.route('/api/owner', methods=['GET'])
def get_owner():
    """Get owner type analysis"""
    return jsonify(MOCK_DATA['owner'])

@app.route('/api/engine', methods=['GET'])
def get_engine():
    """Get engine size analysis"""
    return jsonify(MOCK_DATA['engine'])

@app.route('/api/correlation', methods=['GET'])
def get_correlation():
    """Get feature correlations with price"""
    return jsonify(MOCK_DATA['correlation'])

@app.route('/api/search', methods=['POST'])
def search_cars():
    """Search cars with filters"""
    filters = request.get_json() or {}
    
    # Mock search results
    results = [
        {
            'Name': 'Maruti Swift VDI',
            'Price': 4.5,
            'Year': 2018,
            'Fuel_Type': 'Diesel',
            'Transmission': 'Manual',
            'Owner_Type': 'First',
            'Mileage': 22.5,
            'Engine': 1248,
            'Power': 74,
            'Location': 'Mumbai',
            'Brand': 'Maruti'
        },
        {
            'Name': 'Honda City VX',
            'Price': 7.2,
            'Year': 2019,
            'Fuel_Type': 'Petrol',
            'Transmission': 'Manual',
            'Owner_Type': 'First',
            'Mileage': 17.8,
            'Engine': 1498,
            'Power': 118,
            'Location': 'Delhi',
            'Brand': 'Honda'
        }
    ]
    
    return jsonify({
        'total_found': len(results),
        'results': results,
        'note': 'This is demo data. Full dataset available in the GitHub repository.'
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
