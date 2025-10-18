#!/usr/bin/env python3
"""
Create a sample dataset for Vercel deployment
"""

import pandas as pd
import numpy as np

# Load the original data
df = pd.read_csv('used_cars.csv')

# Create a smaller sample (1000 records)
sample_df = df.sample(n=1000, random_state=42)

# Save the sample
sample_df.to_csv('used_cars_sample.csv', index=False)

print(f"Created sample dataset with {len(sample_df)} records")
print(f"Original size: {len(df)} records")
print("Sample saved as 'used_cars_sample.csv'")
