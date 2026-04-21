import pytest
import pandas as pd
import os
from app import load_data

def test_data_file_exists():
    """Check if the required data file exists"""
    assert os.path.exists('used_cars.csv'), "used_cars.csv not found"

def test_load_data():
    """Test the data loading and cleaning function"""
    df = load_data()
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert 'Brand' in df.columns
    assert 'Price' in df.columns

def test_clean_mileage():
    """Test mileage cleaning logic indirectly via load_data columns if needed, 
    but here we can just check if Mileage is numeric"""
    df = load_data()
    assert pd.api.types.is_numeric_dtype(df['Mileage'])
    assert pd.api.types.is_numeric_dtype(df['Engine'])
    assert pd.api.types.is_numeric_dtype(df['Power'])

def test_basic_math():
    """A dummy test to ensure pytest is working"""
    assert 1 + 1 == 2
