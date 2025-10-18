#!/usr/bin/env python3
"""
Used Cars Analysis - Complete Notebook Execution
This script runs the complete analysis from the Jupyter notebook with all cells
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder, MinMaxScaler, StandardScaler
import plotly.express as px
import warnings
warnings.filterwarnings('ignore')

def main():
    print("="*60)
    print("USED CARS ANALYSIS - CAPSTONE PROJECT")
    print("="*60)
    
    # Cell 1: Imports
    print("\n[Cell 1] Imports completed")
    
    # Cell 2: Reading data and Getting insights
    print("\n[Cell 2] Reading data...")
    df = pd.read_csv('used_cars.csv')
    print(f"Dataset loaded: {df.shape}")
    
    # Cell 3: Display dataframe
    print("\n[Cell 3] Dataset preview:")
    print(df.head())
    
    # Cell 4: Shape
    print(f"\n[Cell 4] Dataset shape: {df.shape}")
    
    # Cell 5: Basic info
    print(f"\n[Cell 5] Rows: {df.shape[0]}, Columns: {df.shape[1]}")
    
    # Cell 6: Info
    print("\n[Cell 6] Dataset info:")
    print(df.info())
    
    # Cell 7: Describe
    print("\n[Cell 7] Statistical summary:")
    print(df.describe().T)
    
    # Cell 8: Unique values
    print("\n[Cell 8] Unique values per column:")
    print(df.nunique())
    
    # Cell 9: Year range
    print(f"\n[Cell 9] Year range: {df['Year'].min()} - {df['Year'].max()}")
    
    # Cell 10: Location distribution
    print("\n[Cell 10] Top 10 locations:")
    print(df['Location'].value_counts().head(10))
    
    # Cell 11: Remove duplicates
    initial_count = len(df)
    df.drop_duplicates(inplace=True)
    print(f"\n[Cell 11] Removed {initial_count - len(df)} duplicate rows")
    
    # Cell 12: Remove unwanted columns
    df.drop(['Unnamed: 0', 'New_Price'], axis=1, inplace=True)
    print("[Cell 12] Removed unwanted columns")
    
    # Cell 13: Data cleaning functions
    def clean_mileage(mileage):
        return float(str(mileage).split()[0]) if pd.notna(mileage) else None

    def clean_engine(engine):
        return float(str(engine).split()[0]) if pd.notna(engine) else None

    def clean_power(power):
        return float(str(power).split()[0]) if pd.notna(power) and power != "null bhp" else None
    
    print("\n[Cell 13] Data cleaning functions defined")
    
    # Cell 14: Clean numerical columns
    df["Mileage"] = df["Mileage"].apply(clean_mileage)
    df["Engine"] = df["Engine"].apply(clean_engine)
    df["Power"] = df["Power"].apply(clean_power)
    print("[Cell 14] Data cleaning completed")
    
    # Cell 15: Fill missing values
    na_cols_to_fill = [x for x in df.columns if df[x].isna().sum() != 0]
    for col in na_cols_to_fill:
        if df[col].dtype in ['float64', 'int64']:
            df[col].fillna(df[col].mean(), inplace=True)
        else:
            df[col].fillna(df[col].mode()[0], inplace=True)
    print("[Cell 15] Missing values filled")
    
    # Cell 16: Create analysis copy
    df_analysis = df.copy()
    print("\n[Cell 16] Analysis copy created")
    
    # Analysis Questions
    print("\n" + "="*50)
    print("ANALYSIS QUESTIONS")
    print("="*50)
    
    # Question 1: Average selling price by brand
    print("\n[Question 1] Average selling price by brand:")
    df_analysis["Brand"] = df_analysis["Name"].apply(lambda x: x.split()[0])
    brand_prices = df_analysis.groupby("Brand")["Price"].mean().sort_values(ascending=False)
    print(brand_prices.head(10))
    
    # Question 2: Cars available per year
    print("\n[Question 2] Cars available per year:")
    cars_per_year = df_analysis["Year"].value_counts().sort_index()
    print(f"Most cars in year: {cars_per_year.idxmax()} ({cars_per_year.max()} cars)")
    print(f"Least cars in year: {cars_per_year.idxmin()} ({cars_per_year.min()} cars)")
    
    # Question 3: Average mileage by fuel type
    print("\n[Question 3] Average mileage by fuel type:")
    mileage_by_fuel = df_analysis.groupby("Fuel_Type")["Mileage"].mean().sort_values(ascending=False)
    print(mileage_by_fuel)
    
    # Question 4: Distribution by transmission type
    print("\n[Question 4] Distribution by transmission type:")
    transmission_dist = df_analysis["Transmission"].value_counts()
    print(transmission_dist)
    
    # Question 5: Owner type analysis
    print("\n[Question 5] Owner type analysis:")
    owner_analysis = df_analysis.groupby("Owner_Type").agg({
        "Name": "count", 
        "Price": "mean"
    }).round(2)
    owner_analysis.columns = ["Car_Count", "Avg_Price"]
    print(owner_analysis)
    
    # Question 6: Year with highest average price
    print("\n[Question 6] Year with highest average selling price:")
    year_prices = df_analysis.groupby("Year")["Price"].mean().sort_values(ascending=False)
    best_year = year_prices.idxmax()
    best_price = year_prices.max()
    print(f"Year: {best_year}, Average Price: Rs.{best_price:.2f}L")
    
    # Question 7: Engine size vs price relationship
    print("\n[Question 7] Engine size vs price relationship:")
    df_analysis["engine_size_bin"] = pd.cut(df_analysis["Engine"], 
                                           bins=[0, 1000, 2000, 3000, 4000, 5000, 6000],
                                           labels=["0-1000", "1000-2000", "2000-3000", "3000-4000", "4000-5000", "5000-6000"])
    engine_price = df_analysis.groupby("engine_size_bin")["Price"].mean().round(2)
    print(engine_price)
    
    # Data Preprocessing for ML
    print("\n" + "="*50)
    print("MACHINE LEARNING PREPROCESSING")
    print("="*50)
    
    # Label encoding
    le = LabelEncoder()
    cat_cols = [x for x in df_analysis.columns if df_analysis[x].dtype == "object" and x != "Name"]
    
    label_mappings = {}
    for col in cat_cols:
        df_analysis[col] = le.fit_transform(df_analysis[col])
        label_mappings[col] = dict(zip(le.classes_, le.transform(le.classes_)))
    
    print("Label encoding completed")
    
    # Log transformation
    numeric_cols = df_analysis.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        if col != "Name":
            df_analysis[col] = np.log1p(df_analysis[col])
    
    print("Log transformation completed")
    
    # Scaling
    scaler = StandardScaler()
    df_scaled = scaler.fit_transform(df_analysis[numeric_cols])
    df_scaled = pd.DataFrame(df_scaled, columns=numeric_cols)
    
    print("Scaling completed")
    
    # Correlation analysis
    print("\nCorrelation Analysis:")
    correlation_matrix = df_scaled.corr()
    price_correlations = correlation_matrix["Price"].abs().sort_values(ascending=False)
    print("Top correlations with Price:")
    print(price_correlations.head(10))
    
    # Summary statistics
    print("\n" + "="*50)
    print("SUMMARY STATISTICS")
    print("="*50)
    print(f"Total cars analyzed: {len(df_analysis)}")
    print(f"Price range: Rs.{df['Price'].min():.2f}L - Rs.{df['Price'].max():.2f}L")
    print(f"Average price: Rs.{df['Price'].mean():.2f}L")
    print(f"Most common fuel type: {df['Fuel_Type'].mode()[0]}")
    print(f"Most common transmission: {df['Transmission'].mode()[0]}")
    print(f"Most common owner type: {df['Owner_Type'].mode()[0]}")
    
    print("\n" + "="*60)
    print("ANALYSIS COMPLETED SUCCESSFULLY!")
    print("="*60)

if __name__ == "__main__":
    main()
