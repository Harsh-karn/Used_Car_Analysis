#!/usr/bin/env python3
"""
Used Cars Analysis - Lightweight Flask API for Vercel
Optimized for serverless deployment
"""

from flask import Flask, jsonify, request, send_file
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
import json
import os

app = Flask(__name__)

# Global variable to store data
df = None

def load_data():
    """Load and preprocess the data on demand"""
    global df
    if df is None:
        try:
            df = pd.read_csv('used_cars.csv')
            
            # Data cleaning functions
            def clean_mileage(mileage):
                return float(str(mileage).split()[0]) if pd.notna(mileage) else None
            def clean_engine(engine):
                return float(str(engine).split()[0]) if pd.notna(engine) else None
            def clean_power(power):
                return float(str(power).split()[0]) if pd.notna(power) and power != "null bhp" else None
            
            # Clean data
            df.drop(['Unnamed: 0', 'New_Price'], axis=1, inplace=True, errors='ignore')
            df["Mileage"] = df["Mileage"].apply(clean_mileage)
            df["Engine"] = df["Engine"].apply(clean_engine)
            df["Power"] = df["Power"].apply(clean_power)
            
            # Fill missing values
            na_cols_to_fill = [x for x in df.columns if df[x].isna().sum() != 0]
            for col in na_cols_to_fill:
                if df[col].dtype in ['float64', 'int64']:
                    df[col].fillna(df[col].mean(), inplace=True)
                else:
                    df[col].fillna(df[col].mode()[0], inplace=True)
            
            # Add brand column
            df['Brand'] = df['Name'].apply(lambda x: x.split()[0])
            
        except Exception as e:
            print(f"Error loading data: {e}")
            # Return sample data if CSV not available
            df = pd.DataFrame({
                'Name': ['Sample Car'],
                'Price': [5.0],
                'Year': [2020],
                'Fuel_Type': ['Petrol'],
                'Transmission': ['Manual'],
                'Owner_Type': ['First'],
                'Mileage': [15.0],
                'Engine': [1200],
                'Power': [85],
                'Location': ['Mumbai'],
                'Brand': ['Sample']
            })
    
    return df

@app.route('/')
def home():
    """Home page - serve index.html"""
    if os.path.exists('index.html'):
        return send_file('index.html')
    else:
        return jsonify({
            "message": "Used Cars Analysis API",
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
    df = load_data()
    stats = {
        'total_cars': len(df),
        'average_price': float(df['Price'].mean()),
        'price_range': {
            'min': float(df['Price'].min()),
            'max': float(df['Price'].max())
        },
        'year_range': {
            'min': int(df['Year'].min()),
            'max': int(df['Year'].max())
        },
        'unique_brands': int(df['Brand'].nunique()),
        'most_common_fuel': df['Fuel_Type'].mode()[0],
        'most_common_transmission': df['Transmission'].mode()[0]
    }
    return jsonify(stats)

@app.route('/api/brands', methods=['GET'])
def get_brands():
    """Get brand analysis"""
    df = load_data()
    brand_prices = df.groupby('Brand')['Price'].mean().sort_values(ascending=False)
    brand_counts = df['Brand'].value_counts()
    
    result = []
    for brand in brand_prices.index[:20]:  # Limit to top 20
        result.append({
            'brand': brand,
            'average_price': float(brand_prices[brand]),
            'count': int(brand_counts[brand])
        })
    
    return jsonify(result)

@app.route('/api/years', methods=['GET'])
def get_years():
    """Get year analysis"""
    df = load_data()
    year_counts = df['Year'].value_counts().sort_index()
    year_prices = df.groupby('Year')['Price'].mean()
    
    result = []
    for year in year_counts.index:
        result.append({
            'year': int(year),
            'count': int(year_counts[year]),
            'average_price': float(year_prices[year])
        })
    
    return jsonify(result)

@app.route('/api/fuel', methods=['GET'])
def get_fuel():
    """Get fuel type analysis"""
    df = load_data()
    fuel_mileage = df.groupby('Fuel_Type')['Mileage'].mean().sort_values(ascending=False)
    fuel_counts = df['Fuel_Type'].value_counts()
    fuel_prices = df.groupby('Fuel_Type')['Price'].mean()
    
    result = []
    for fuel in fuel_mileage.index:
        result.append({
            'fuel_type': fuel,
            'average_mileage': float(fuel_mileage[fuel]),
            'count': int(fuel_counts[fuel]),
            'average_price': float(fuel_prices[fuel])
        })
    
    return jsonify(result)

@app.route('/api/transmission', methods=['GET'])
def get_transmission():
    """Get transmission analysis"""
    df = load_data()
    trans_counts = df['Transmission'].value_counts()
    trans_prices = df.groupby('Transmission')['Price'].mean()
    
    result = []
    for trans in trans_counts.index:
        result.append({
            'transmission': trans,
            'count': int(trans_counts[trans]),
            'average_price': float(trans_prices[trans])
        })
    
    return jsonify(result)

@app.route('/api/owner', methods=['GET'])
def get_owner():
    """Get owner type analysis"""
    df = load_data()
    owner_analysis = df.groupby('Owner_Type').agg({
        'Name': 'count',
        'Price': 'mean'
    })
    
    result = []
    for owner in owner_analysis.index:
        result.append({
            'owner_type': owner,
            'count': int(owner_analysis.loc[owner, 'Name']),
            'average_price': float(owner_analysis.loc[owner, 'Price'])
        })
    
    return jsonify(result)

@app.route('/api/engine', methods=['GET'])
def get_engine():
    """Get engine size analysis"""
    df = load_data()
    df_engine = df.copy()
    df_engine['engine_size_bin'] = pd.cut(df_engine['Engine'], 
                                         bins=[0, 1000, 2000, 3000, 4000, 5000, 6000],
                                         labels=['0-1000', '1000-2000', '2000-3000', '3000-4000', '4000-5000', '5000-6000'])
    
    engine_analysis = df_engine.groupby('engine_size_bin')['Price'].mean()
    
    result = []
    for bin_range in engine_analysis.index:
        if pd.notna(bin_range):
            result.append({
                'engine_range': str(bin_range),
                'average_price': float(engine_analysis[bin_range])
            })
    
    return jsonify(result)

@app.route('/api/correlation', methods=['GET'])
def get_correlation():
    """Get feature correlations with price"""
    df = load_data()
    df_ml = df.copy()
    le = LabelEncoder()
    cat_cols = ['Location', 'Fuel_Type', 'Transmission', 'Owner_Type']
    
    for col in cat_cols:
        if col in df_ml.columns:
            df_ml[col] = le.fit_transform(df_ml[col])
    
    numeric_cols = df_ml.select_dtypes(include=[np.number]).columns
    correlation_matrix = df_ml[numeric_cols].corr()
    
    price_correlations = correlation_matrix['Price'].abs().sort_values(ascending=False)
    
    result = []
    for feature, correlation in price_correlations.items():
        if feature != 'Price':
            result.append({
                'feature': feature,
                'correlation': float(correlation)
            })
    
    return jsonify(result)

@app.route('/api/search', methods=['POST'])
def search_cars():
    """Search cars with filters"""
    df = load_data()
    filters = request.get_json() or {}
    
    filtered_df = df.copy()
    
    if 'brand' in filters:
        filtered_df = filtered_df[filtered_df['Brand'].str.contains(filters['brand'], case=False, na=False)]
    
    if 'fuel_type' in filters:
        filtered_df = filtered_df[filtered_df['Fuel_Type'] == filters['fuel_type']]
    
    if 'transmission' in filters:
        filtered_df = filtered_df[filtered_df['Transmission'] == filters['transmission']]
    
    if 'min_price' in filters:
        filtered_df = filtered_df[filtered_df['Price'] >= filters['min_price']]
    
    if 'max_price' in filters:
        filtered_df = filtered_df[filtered_df['Price'] <= filters['max_price']]
    
    if 'min_year' in filters:
        filtered_df = filtered_df[filtered_df['Year'] >= filters['min_year']]
    
    if 'max_year' in filters:
        filtered_df = filtered_df[filtered_df['Year'] <= filters['max_year']]
    
    # Convert to JSON serializable format
    result = filtered_df.head(100).to_dict('records')
    
    return jsonify({
        'total_found': len(filtered_df),
        'results': result
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
