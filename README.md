# Task_03_Descriptive_Stats

This repository contains Python scripts for "Research Task 3: Descriptive Statistics with and without 3rd Party Libraries (Pandas/Polars)". The goal was to summarize social media datasets related to the 2024 US presidential elections using different Python approaches.

1. Instructions to Run
Prerequisites

Python 3.9+

pip (Python package installer)

Library Installation

Install the required libraries:

pip install pandas polars matplotlib seaborn

Dataset Placement

Download the three CSV files from the provided Google Drive link:
https://drive.google.com/file/d/1Jq0fPb-tq76Ee_RtM58fT0_M3o-JDBwe/view?usp=sharing

Place all three CSV files (2024_fb_ads_president_scored_anon.csv, 2024_fb_posts_president_scored_anon.csv, 2024_tw_posts_president_scored_anon.csv) into a directory on your local machine.

Important: Update the base_directory variable within each Python script (pure_python_stats.py, pandas_stats.py, polars_stats.py) to the absolute path of your dataset directory.

Example:

base_directory = "/Users/YourUser/Downloads/Task_03_Descriptive_Stats/" # Update this line

Running the Scripts

Execute each script from the repository's root directory in your terminal. Redirect output to text files for complete capture:

python pure_python_stats.py > pure_python_output.txt
python pandas_stats.py > pandas_output.txt
python polars_stats.py > polars_output.txt
# python visualization_script.py # Run if you have a separate visualization script

2. Summary of Findings and Insights
This analysis highlighted key differences in data processing capabilities across pure Python, Pandas, and Polars.

Data Loading Robustness: Pandas and Polars demonstrated superior ability to load and correctly interpret large, real-world CSV files compared to the custom pure Python implementation, which struggled with some datasets. This is due to their optimized, low-level backends.

Ease of Use & Conciseness: Pandas and Polars significantly simplify data manipulation and statistical computation with their high-level APIs (.describe(), .value_counts(), .groupby()). Pure Python requires more manual coding for similar results.

Performance: While direct time measurements were not reported, the inherent design of Pandas (C-optimized) and especially Polars (Rust-optimized, with query optimization) suggests they are much faster and more memory-efficient for large datasets than pure Python loops.

Challenges: Initial errors in both Pandas (due to idxmax() on empty groups) and Polars (due to incorrect column naming for sorting value_counts()) were successfully resolved by implementing robust error handling and correct API usage. Grouped analyses were sometimes skipped if expected grouping columns were not found in a specific dataset.

Dataset Insights:

The Twitter dataset (2024_tw_posts_president_scored_anon.csv) was the largest and most complete, showing clear distributions of interaction counts (retweets, likes, replies, views). A significant portion of tweets originated from "Twitter Web App" and were in English.

The Facebook Ads and Posts datasets revealed detailed information about ad performance metrics, bylines, and page categories. The presence of nested JSON-like strings in columns like delivery_by_region and demographic_distribution highlights the need for data unpacking.

Common columns across datasets (e.g., related to page_id, message content, and topic illuminations) provide opportunities for cross-platform comparative analysis.

For data analysis tasks, Pandas is highly recommended for its ease of use and broad functionality, making it ideal for junior analysts. Polars is an excellent choice for performance-critical scenarios. Pure Python is valuable for understanding fundamentals but less practical for complex, large-scale data analysis.
