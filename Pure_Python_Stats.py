import csv
import math
import os # For path manipulation and checking file existence
from collections import defaultdict, Counter
from typing import List, Dict, Any, Tuple
import json # For potential JSON output

# --- Helper Functions (Defined once) ---

# Load the CSV file
def load_csv(filepath: str) -> Tuple[List[str], List[Dict[str, Any]]]:
    """
    Loads a CSV file into a list of dictionaries (rows) and a list of headers.
    """
    with open(filepath, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        rows = [row for row in reader]
        headers = reader.fieldnames if reader.fieldnames else [] # Handle case of empty file or no headers
    return headers, rows

# Convert to float if possible, otherwise return the stripped string
def try_parse_float(value: str) -> Any:
    """
    Attempts to convert a string value to a float.
    Returns float if successful, None if value is None or empty,
    otherwise returns the original stripped string.
    """
    if value is None or (isinstance(value, str) and value.strip() == ''):
        return None
    try:
        return float(value)
    except ValueError:
        return value.strip()

# Compute stats for a column
def compute_stats(values: List[Any]) -> Dict[str, Any]:
    """
    Computes basic descriptive statistics for a list of values.
    Separates numeric and non-numeric values for different stats.
    Handles None values by filtering them out before calculation.
    """
    # Filter out None values before processing, as they can cause issues with stats
    filtered_values = [v for v in values if v is not None]

    numeric_values = [v for v in filtered_values if isinstance(v, (float, int))]
    non_numeric_values = [v for v in filtered_values if not isinstance(v, (float, int))]
    
    stats = {'total_count': len(filtered_values)} # Count based on non-None values
    
    if numeric_values:
        stats['numeric_count'] = len(numeric_values)
        stats['mean'] = sum(numeric_values) / len(numeric_values)
        stats['min'] = min(numeric_values)
        stats['max'] = max(numeric_values)
        if len(numeric_values) > 1:
            mean = stats['mean']
            # Calculate sample standard deviation (n-1 degrees of freedom)
            variance = sum((x - mean) ** 2 for x in numeric_values) / (len(numeric_values) - 1)
            stats['stddev'] = math.sqrt(variance)
        else:
            # Standard deviation is 0 for a single data point, or None for empty
            stats['stddev'] = 0.0 if len(numeric_values) == 1 else None
    else:
        stats['numeric_count'] = 0
        stats['mean'] = None
        stats['min'] = None
        stats['max'] = None
        stats['stddev'] = None

    if non_numeric_values:
        counter = Counter(non_numeric_values)
        stats['non_numeric_count'] = len(non_numeric_values)
        stats['unique_non_numeric'] = len(counter)
        # most_common returns a list of (value, count) tuples. Get the first one.
        stats['most_common_non_numeric'] = counter.most_common(1)[0] if counter else None
    else:
        stats['non_numeric_count'] = 0
        stats['unique_non_numeric'] = 0
        stats['most_common_non_numeric'] = None
    
    return stats

# Analyze all columns in the dataset
def analyze_dataset(headers: List[str], rows: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    """
    Analyzes each column in the dataset and computes statistics.
    Handles cases where a row might not contain a header, appending None.
    """
    columns = defaultdict(list)
    for row in rows:
        for h in headers:
            # Ensure the key exists in the row before trying to access it
            # csv.DictReader might fill missing fields with empty strings, but explicit check is safer
            value = try_parse_float(row.get(h, None)) # Use .get() with a default of None
            columns[h].append(value)
    
    summary = {}
    for col, values in columns.items():
        summary[col] = compute_stats(values)
    return summary

# Group by one or more columns
def group_by(rows: List[Dict[str, Any]], keys: List[str]) -> Dict[Tuple, List[Dict[str, Any]]]:
    """
    Groups rows by the specified key columns.
    Applies try_parse_float to key values to ensure consistent type for grouping.
    Handles missing keys in a row by using None.
    """
    grouped = defaultdict(list)
    for row in rows:
        key_values = []
        for k in keys:
            # Get the key value, apply try_parse_float, and handle missing keys
            key_values.append(try_parse_float(row.get(k, None)))
        key = tuple(key_values)
        grouped[key].append(row)
    return grouped

# Analyze grouped data
def analyze_groups(headers: List[str], rows: List[Dict[str, Any]], group_keys: List[str]) -> Dict:
    """
    Groups the data and then analyzes each group.
    """
    # Pre-check if all group_keys exist in headers for informational purposes
    missing_keys = [key for key in group_keys if key not in headers]
    if missing_keys:
        print(f"Warning: Grouping keys {missing_keys} not found in dataset headers. These groups will use 'None' for missing keys.")

    grouped_data = group_by(rows, group_keys)
    group_summaries = {}
    for group, group_rows in grouped_data.items():
        # Pass the original full headers for consistency with analyze_dataset
        group_summary = analyze_dataset(headers, group_rows)
        group_summaries[group] = group_summary
    return group_summaries

# Convert tuple keys to strings for JSON output (useful if saving results)
def stringify_keys(d: Dict[Tuple, Any]) -> Dict[str, Any]:
    return {str(k): v for k, v in d.items()}

# ======= Main Execution Logic =======

if __name__ == "__main__":
    # Define your datasets and base directory
    datasets_to_analyze = [
        "/Users/Guest/Downloads/Task_03_Descriptive_Stats/2024_fb_ads_president_scored_anon.csv",
        "/Users/Guest/Downloads/Task_03_Descriptive_Stats/2024_fb_posts_president_scored_anon.csv",
        "/Users/Guest/Downloads/Task_03_Descriptive_Stats/2024_tw_posts_president_scored_anon.csv"
    ]

    # Base directory for your files (Adjust this to your actual path)
    # Based on your path /Users/namrathaaddala/Downloads/period_03/...
    base_directory = "/Users/namrathaaddala/Downloads/period_03/"

    # Dictionary to store all results for potential JSON export
    all_analysis_results = {}

    for dataset_file_name in datasets_to_analyze:
        file_path = os.path.join(base_directory, dataset_file_name)

        print(f"\n\n--- Processing Dataset: {dataset_file_name} ---")
        print(f"Full path: {file_path}")

        if not os.path.exists(file_path):
            print(f"Error: File not found at '{file_path}'. Skipping to next dataset.")
            continue # Skip to the next file if this one doesn't exist

        try:
            headers, rows = load_csv(file_path)
            print(f"Loaded {len(rows)} rows with {len(headers)} columns.")

            current_dataset_results = {}

            # --- Overall analysis ---
            print("\n=== Overall Stats ===")
            overall_stats = analyze_dataset(headers, rows)
            current_dataset_results['overall_stats'] = overall_stats
            for col, stats in overall_stats.items():
                print(f"--- Column: {col} ---")
                for stat_name, stat_value in stats.items():
                    if isinstance(stat_value, float):
                        print(f"  {stat_name}: {stat_value:.4f}")
                    else:
                        print(f"  {stat_name}: {stat_value}")


            # --- Group by 'page_id' (if available) ---
            # Check for different possible naming conventions based on your previous code
            page_id_col = None
            if "page_id" in headers:
                page_id_col = "page_id"
            elif "Facebook_Id" in headers: # From your second snippet
                page_id_col = "Facebook_Id"

            if page_id_col:
                print(f"\n\n=== Sample Grouped by '{page_id_col}' ===")
                grouped_by_page = analyze_groups(headers, rows, [page_id_col])
                current_dataset_results[f'grouped_by_{page_id_col}'] = stringify_keys(grouped_by_page) # Store full dict
                # Only show first 2 groups for brevity in console
                for key, summary in list(grouped_by_page.items())[:2]:
                    print(f"\nGroup: {key}")
                    for col, stats in summary.items():
                        print(f"  --- Column: {col} ---")
                        for stat_name, stat_value in stats.items():
                            if isinstance(stat_value, float):
                                print(f"    {stat_name}: {stat_value:.4f}")
                            else:
                                print(f"    {stat_name}: {stat_value}")
            else:
                print(f"\nSkipping 'Group by page_id' as neither 'page_id' nor 'Facebook_Id' column found.")


            # --- Group by ['page_id', 'ad_id'] or ['Facebook_Id', 'post_id'] (if available) ---
            ad_id_col = None
            post_id_col = None
            if "ad_id" in headers:
                ad_id_col = "ad_id"
            if "post_id" in headers: # From your second snippet
                post_id_col = "post_id"

            group_keys_combined = []
            if page_id_col:
                group_keys_combined.append(page_id_col)
            if ad_id_col:
                group_keys_combined.append(ad_id_col)
            elif post_id_col: # If ad_id not found, try post_id
                group_keys_combined.append(post_id_col)

            if len(group_keys_combined) >= 2: # Ensure we have at least two keys for combined grouping
                print(f"\n\n=== Sample Grouped by {group_keys_combined} ===")
                grouped_by_combined = analyze_groups(headers, rows, group_keys_combined)
                current_dataset_results[f'grouped_by_{"_".join(group_keys_combined)}'] = stringify_keys(grouped_by_combined) # Store full dict
                # Only show first 2 groups for brevity in console
                for key, summary in list(grouped_by_combined.items())[:2]:
                    print(f"\nGroup: {key}")
                    for col, stats in summary.items():
                        print(f"  --- Column: {col} ---")
                        for stat_name, stat_value in stats.items():
                            if isinstance(stat_value, float):
                                print(f"    {stat_name}: {stat_value:.4f}")
                            else:
                                print(f"    {stat_name}: {stat_value}")
            else:
                print(f"\nSkipping 'Group by combined keys' as required columns not found (need at least two: {page_id_col} and ad_id/post_id).")

            # Store results for this dataset
            all_analysis_results[dataset_file_name] = current_dataset_results

        except Exception as e:
            print(f"An unexpected error occurred while processing {dataset_file_name}: {e}")

    # --- Optional: Save all results to a single JSON file ---
    output_json_path = os.path.join(base_directory, "all_datasets_summary.json")
    try:
        with open(output_json_path, "w", encoding="utf-8") as f:
            json.dump(all_analysis_results, f, indent=2)
        print(f"\n\nAll analysis results saved to: {output_json_path}")
    except Exception as e:
        print(f"\nError saving all results to JSON: {e}")

    print("\n--- All Dataset Analysis Complete ---")