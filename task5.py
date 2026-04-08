# task2_data_processing.py
# TrendPulse: Clean raw JSON data and save as CSV

import pandas as pd
import os
from datetime import datetime

# --- Step 1: Load JSON file ---
# Find today's file (same format from Task 1)
date_str = datetime.now().strftime('%Y%m%d')
file_path = f"/Users/gauravadarkar/Downloads/AI_Projects/trendpulse-GauravAdarkar/data/trends_20260406.json"

try:
    df = pd.read_json(file_path)
    print(f"Loaded {len(df)} stories from {file_path}")
except Exception as e:
    print("Error loading file:", e)
    exit()

# --- Step 2: Data Cleaning ---

# 1. Remove duplicates based on post_id
before = len(df)
df = df.drop_duplicates(subset="post_id")
print(f"After removing duplicates: {len(df)}")

# 2. Remove missing values (important columns)
df = df.dropna(subset=["post_id", "title", "score"])
print(f"After removing nulls: {len(df)}")

# 3. Fix data types
df["score"] = df["score"].astype(int)
df["num_comments"] = df["num_comments"].astype(int)

# 4. Remove low-quality posts (score < 5)
df = df[df["score"] >= 5]
print(f"After removing low scores: {len(df)}")

# 5. Clean text (remove extra spaces in title)
df["title"] = df["title"].str.strip()

# --- Step 3: Save cleaned data ---
os.makedirs("data", exist_ok=True)
output_file = "data/trends_clean.csv"

df.to_csv(output_file, index=False)

print(f"Saved {len(df)} rows to {output_file}")

# --- Step 4: Summary ---
print("\nStories per category:")
print(df["category"].value_counts())