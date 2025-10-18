#!/usr/bin/env python3
"""
Used Cars Analysis - Visualization Script
Creates charts and visualizations for the used cars dataset
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import warnings
warnings.filterwarnings('ignore')

def create_visualizations():
    print("Creating visualizations...")
    
    # Read and clean data
    df = pd.read_csv('used_cars.csv')
    df.drop(['Unnamed: 0', 'New_Price'], axis=1, inplace=True)
    
    # Clean data
    def clean_mileage(mileage):
        return float(str(mileage).split()[0]) if pd.notna(mileage) else None
    def clean_engine(engine):
        return float(str(engine).split()[0]) if pd.notna(engine) else None
    def clean_power(power):
        return float(str(power).split()[0]) if pd.notna(power) and power != "null bhp" else None
    
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
    
    # Set style
    plt.style.use('default')
    sns.set_palette("husl")
    
    # 1. Price distribution
    plt.figure(figsize=(12, 8))
    plt.subplot(2, 2, 1)
    plt.hist(df['Price'], bins=50, alpha=0.7, color='skyblue', edgecolor='black')
    plt.title('Price Distribution')
    plt.xlabel('Price (Lakhs)')
    plt.ylabel('Frequency')
    
    # 2. Cars by year
    plt.subplot(2, 2, 2)
    year_counts = df['Year'].value_counts().sort_index()
    plt.bar(year_counts.index, year_counts.values, color='lightgreen', alpha=0.7)
    plt.title('Cars Available by Year')
    plt.xlabel('Year')
    plt.ylabel('Number of Cars')
    plt.xticks(rotation=45)
    
    # 3. Fuel type distribution
    plt.subplot(2, 2, 3)
    fuel_counts = df['Fuel_Type'].value_counts()
    plt.pie(fuel_counts.values, labels=fuel_counts.index, autopct='%1.1f%%', startangle=90)
    plt.title('Distribution by Fuel Type')
    
    # 4. Transmission distribution
    plt.subplot(2, 2, 4)
    trans_counts = df['Transmission'].value_counts()
    plt.bar(trans_counts.index, trans_counts.values, color=['orange', 'purple'], alpha=0.7)
    plt.title('Transmission Type Distribution')
    plt.xlabel('Transmission')
    plt.ylabel('Count')
    
    plt.tight_layout()
    plt.savefig('used_cars_overview.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # 5. Brand analysis
    df['Brand'] = df['Name'].apply(lambda x: x.split()[0])
    brand_prices = df.groupby('Brand')['Price'].mean().sort_values(ascending=False).head(15)
    
    plt.figure(figsize=(15, 8))
    plt.barh(range(len(brand_prices)), brand_prices.values, color='coral', alpha=0.7)
    plt.yticks(range(len(brand_prices)), brand_prices.index)
    plt.title('Average Price by Brand (Top 15)')
    plt.xlabel('Average Price (Lakhs)')
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.savefig('brand_prices.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # 6. Correlation heatmap
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    correlation_matrix = df[numeric_cols].corr()
    
    plt.figure(figsize=(12, 10))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0, 
                square=True, fmt='.2f', cbar_kws={'shrink': 0.8})
    plt.title('Correlation Matrix of Numerical Features')
    plt.tight_layout()
    plt.savefig('correlation_heatmap.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # 7. Price vs Engine size
    plt.figure(figsize=(12, 6))
    plt.scatter(df['Engine'], df['Price'], alpha=0.6, color='blue')
    plt.title('Price vs Engine Size')
    plt.xlabel('Engine Size (CC)')
    plt.ylabel('Price (Lakhs)')
    plt.tight_layout()
    plt.savefig('price_vs_engine.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # 8. Box plots for categorical variables
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    
    # Fuel Type vs Price
    sns.boxplot(data=df, x='Fuel_Type', y='Price', ax=axes[0,0])
    axes[0,0].set_title('Price by Fuel Type')
    axes[0,0].tick_params(axis='x', rotation=45)
    
    # Transmission vs Price
    sns.boxplot(data=df, x='Transmission', y='Price', ax=axes[0,1])
    axes[0,1].set_title('Price by Transmission')
    
    # Owner Type vs Price
    sns.boxplot(data=df, x='Owner_Type', y='Price', ax=axes[1,0])
    axes[1,0].set_title('Price by Owner Type')
    axes[1,0].tick_params(axis='x', rotation=45)
    
    # Year vs Price (sample of years)
    year_sample = df[df['Year'] >= 2010].copy()
    sns.boxplot(data=year_sample, x='Year', y='Price', ax=axes[1,1])
    axes[1,1].set_title('Price by Year (2010+)')
    axes[1,1].tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    plt.savefig('categorical_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    print("Visualizations created and saved as PNG files!")
    print("Files created:")
    print("- used_cars_overview.png")
    print("- brand_prices.png") 
    print("- correlation_heatmap.png")
    print("- price_vs_engine.png")
    print("- categorical_analysis.png")

if __name__ == "__main__":
    create_visualizations()
