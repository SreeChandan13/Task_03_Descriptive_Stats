#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import polars as pl
import os # Import the os module to construct file paths and check existence

# --- Configuration ---
# Your list of dataset filenames
datasets = [
    "/Users/Guest/Downloads/Task_03_Descriptive_Stats/2024_fb_ads_president_scored_anon.csv",
    "/Users/Guest/Downloads/Task_03_Descriptive_Stats/2024_fb_posts_president_scored_anon.csv",
    "/Users/Guest/Downloads/Task_03_Descriptive_Stats/2024_tw_posts_president_scored_anon.csv"
]

# The base directory where all these CSV files are located
# This path is derived from your original snippets. Please ensure it's correct.
base_directory = "/Users/Guest/Downloads/Task_03_Descriptive_Stats/"

# --- Loop through each dataset and perform analysis ---
for dataset_name in datasets:
    file_path = os.path.join(base_directory, dataset_name)

    print(f"\n\n--- Analyzing Dataset: {dataset_name} with Polars ---")
    print(f"Full path: {file_path}")

    # Check if the file exists before attempting to load
    if not os.path.exists(file_path):
        print(f"Error: The file was not found at '{file_path}'. Skipping this dataset.")
        continue # Move to the next dataset in the list

    try:
        # Step 1: Load the dataset
        df = pl.read_csv(file_path)
        print("Polars DataFrame loaded successfully.")
        print(f"DataFrame shape: {df.shape}")

        # Step 2A: Use describe() for numeric summary
        print("\n=== Numeric Summary ===")
        # Polars describe() provides a good overview for both numeric and string columns
        # You can filter it if you only want numeric, but it's usually comprehensive.
        print(df.describe())

        # Step 2B: value_counts() and nunique() for categorical/Utf8 columns
        print("\n=== Categorical Value Counts and Unique Counts ===")

        # Loop through columns and identify Utf8 (string) type
        for col in df.columns:
            if df[col].dtype == pl.Utf8:
                print(f"\n--- Column: {col} ---")
                try:
                    # Check if the column itself is empty (no rows of data)
                    if df[col].is_empty():
                        print(f"Column '{col}' is empty.")
                        continue

                    # FIX: Use group_by().agg() to explicitly name the count column for sorting.
                    # This avoids the "ColumnNotFoundError: 'counts' not found" issue.
                    # pl.len() is used to count rows within each group, and .alias() renames it.
                    value_counts_df = df.group_by(col).agg(pl.len().alias("count_of_values"))

                    # Now sort by the explicitly named count column
                    # Handle case where value_counts_df might be empty if all values are null/empty after group_by
                    if value_counts_df.is_empty():
                        print(f"No unique values found or counted for column '{col}'.")
                    else:
                        print("Top 5 Most Frequent Values:")
                        # Ensure to sort by the aliased column name
                        print(value_counts_df.sort("count_of_values", descending=True).head(5))

                    # Get unique count (n_unique() automatically handles nulls if present)
                    print(f"Number of Unique Values: {df[col].n_unique()}")

                except Exception as e:
                    print(f"Error processing column '{col}' for value counts: {e}")

    except pl.exceptions.NoDataError:
        print(f"Error: The CSV file '{file_path}' is empty or contains no valid data for Polars.")
    except pl.exceptions.ComputeError as e:
        print(f"Error during Polars computation for {dataset_name}: {e}")
    except Exception as e:
        print(f"An unexpected error occurred during Polars analysis for {dataset_name}: {e}")

print("\n\n--- All Dataset Analysis Complete ---")