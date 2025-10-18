#!/usr/bin/env python3
"""
Used Cars Analysis - Streamlit Web Application
Deployable web app for the capstone project
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from sklearn.preprocessing import LabelEncoder, StandardScaler
import warnings
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="Used Cars Analysis",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .insight-box {
        background-color: #e8f4fd;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #ff6b6b;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Load and preprocess the data"""
    df = pd.read_csv('used_cars.csv')
    
    # Data cleaning functions
    def clean_mileage(mileage):
        return float(str(mileage).split()[0]) if pd.notna(mileage) else None
    def clean_engine(engine):
        return float(str(engine).split()[0]) if pd.notna(engine) else None
    def clean_power(power):
        return float(str(power).split()[0]) if pd.notna(power) and power != "null bhp" else None
    
    # Clean data
    df.drop(['Unnamed: 0', 'New_Price'], axis=1, inplace=True)
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
    
    return df

def main():
    # Header
    st.markdown('<h1 class="main-header">🚗 Used Cars Analysis Dashboard</h1>', unsafe_allow_html=True)
    st.markdown("### Capstone Project - Data Science Analysis")
    
    # Load data
    with st.spinner('Loading data...'):
        df = load_data()
    
    # Sidebar
    st.sidebar.title("📊 Analysis Controls")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Cars", f"{len(df):,}")
    
    with col2:
        st.metric("Average Price", f"₹{df['Price'].mean():.2f}L")
    
    with col3:
        st.metric("Year Range", f"{df['Year'].min()}-{df['Year'].max()}")
    
    with col4:
        st.metric("Unique Brands", f"{df['Brand'].nunique()}")
    
    # Main tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📈 Overview", "🔍 Analysis", "📊 Visualizations", "🤖 ML Insights", "📋 Data Explorer"])
    
    with tab1:
        st.header("📈 Dataset Overview")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Dataset Information")
            st.write(f"**Shape:** {df.shape[0]} rows × {df.shape[1]} columns")
            st.write(f"**Price Range:** ₹{df['Price'].min():.2f}L - ₹{df['Price'].max():.2f}L")
            st.write(f"**Most Common Fuel:** {df['Fuel_Type'].mode()[0]}")
            st.write(f"**Most Common Transmission:** {df['Transmission'].mode()[0]}")
        
        with col2:
            st.subheader("Top Locations")
            location_counts = df['Location'].value_counts().head(10)
            fig = px.bar(x=location_counts.values, y=location_counts.index, 
                        orientation='h', title="Cars by Location")
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.header("🔍 Business Analysis")
        
        # Question 1: Brand Analysis
        st.subheader("1. Average Price by Brand")
        brand_prices = df.groupby('Brand')['Price'].mean().sort_values(ascending=False).head(10)
        
        col1, col2 = st.columns(2)
        with col1:
            st.dataframe(brand_prices.round(2))
        with col2:
            fig = px.bar(x=brand_prices.values, y=brand_prices.index, 
                        orientation='h', title="Top 10 Brands by Average Price")
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        # Question 2: Year Analysis
        st.subheader("2. Cars Available by Year")
        year_counts = df['Year'].value_counts().sort_index()
        
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Most cars in:** {year_counts.idxmax()} ({year_counts.max()} cars)")
            st.write(f"**Least cars in:** {year_counts.idxmin()} ({year_counts.min()} cars)")
        with col2:
            fig = px.line(x=year_counts.index, y=year_counts.values, 
                         title="Cars Available by Year")
            st.plotly_chart(fig, use_container_width=True)
        
        # Question 3: Fuel Type Analysis
        st.subheader("3. Mileage by Fuel Type")
        mileage_by_fuel = df.groupby('Fuel_Type')['Mileage'].mean().sort_values(ascending=False)
        
        col1, col2 = st.columns(2)
        with col1:
            st.dataframe(mileage_by_fuel.round(2))
        with col2:
            fig = px.pie(values=mileage_by_fuel.values, names=mileage_by_fuel.index, 
                        title="Average Mileage by Fuel Type")
            st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.header("📊 Interactive Visualizations")
        
        # Price distribution
        st.subheader("Price Distribution")
        fig = px.histogram(df, x='Price', nbins=50, title="Price Distribution")
        st.plotly_chart(fig, use_container_width=True)
        
        # Price vs Engine
        st.subheader("Price vs Engine Size")
        fig = px.scatter(df, x='Engine', y='Price', color='Fuel_Type', 
                        title="Price vs Engine Size by Fuel Type")
        st.plotly_chart(fig, use_container_width=True)
        
        # Transmission analysis
        st.subheader("Transmission Distribution")
        trans_counts = df['Transmission'].value_counts()
        fig = px.pie(values=trans_counts.values, names=trans_counts.index, 
                    title="Transmission Type Distribution")
        st.plotly_chart(fig, use_container_width=True)
    
    with tab4:
        st.header("🤖 Machine Learning Insights")
        
        # Correlation analysis
        st.subheader("Feature Correlations with Price")
        
        # Prepare data for correlation
        df_ml = df.copy()
        le = LabelEncoder()
        cat_cols = ['Location', 'Fuel_Type', 'Transmission', 'Owner_Type']
        
        for col in cat_cols:
            df_ml[col] = le.fit_transform(df_ml[col])
        
        numeric_cols = df_ml.select_dtypes(include=[np.number]).columns
        correlation_matrix = df_ml[numeric_cols].corr()
        
        # Top correlations with price
        price_correlations = correlation_matrix['Price'].abs().sort_values(ascending=False).head(10)
        
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Top Correlations with Price")
            st.dataframe(price_correlations.round(3))
        
        with col2:
            fig = px.bar(x=price_correlations.values, y=price_correlations.index, 
                        orientation='h', title="Feature Correlations with Price")
            st.plotly_chart(fig, use_container_width=True)
        
        # Insights
        st.subheader("🔍 Key Insights")
        insights = [
            f"**Power** has the strongest correlation with price ({price_correlations['Power']:.3f})",
            f"**Engine size** is the second strongest predictor ({price_correlations['Engine']:.3f})",
            f"**Transmission type** significantly affects price ({price_correlations['Transmission']:.3f})",
            f"**Year** shows moderate correlation with price ({price_correlations['Year']:.3f})"
        ]
        
        for insight in insights:
            st.markdown(f"• {insight}")
    
    with tab5:
        st.header("📋 Data Explorer")
        
        # Filters
        st.subheader("Filter Data")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            selected_brands = st.multiselect("Select Brands", df['Brand'].unique(), default=df['Brand'].unique()[:5])
        
        with col2:
            selected_fuel = st.multiselect("Select Fuel Types", df['Fuel_Type'].unique(), default=df['Fuel_Type'].unique())
        
        with col3:
            price_range = st.slider("Price Range (Lakhs)", 
                                  float(df['Price'].min()), 
                                  float(df['Price'].max()), 
                                  (float(df['Price'].min()), float(df['Price'].max())))
        
        # Apply filters
        filtered_df = df[
            (df['Brand'].isin(selected_brands)) &
            (df['Fuel_Type'].isin(selected_fuel)) &
            (df['Price'] >= price_range[0]) &
            (df['Price'] <= price_range[1])
        ]
        
        st.subheader(f"Filtered Data ({len(filtered_df)} cars)")
        st.dataframe(filtered_df.head(100))
        
        # Download button
        csv = filtered_df.to_csv(index=False)
        st.download_button(
            label="Download Filtered Data as CSV",
            data=csv,
            file_name='filtered_used_cars.csv',
            mime='text/csv'
        )
    
    # Footer
    st.markdown("---")
    st.markdown("### 🎓 Capstone Project - Used Cars Analysis")
    st.markdown("**Technologies:** Python, Pandas, Streamlit, Plotly, Scikit-learn")
    st.markdown("**Dataset:** 6,019 used car records from 1998-2019")

if __name__ == "__main__":
    main()
