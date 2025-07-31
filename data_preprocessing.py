# data_preprocessing.py

import pandas as pd
import requests # Keep this for potential future download functionality if needed
import os # Keep this for path manipulation if needed

def load_and_preprocess_data(file_path):
    """
    Loads e-commerce interaction data and performs basic preprocessing.
    Assumes CSV file with no header and the four columns in the order:
    'user_id', 'product_id', 'rating', and 'timestamp'.
    """
    print(f"Loading data from: {file_path}")

    try:
        # Load the CSV, explicitly naming the columns and indicating no header
        # This is the key change to handle your dataset format
        df = pd.read_csv(file_path, header=None, names=['user_id', 'product_id', 'rating', 'timestamp'])
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}. Please check the path and filename.")
        return None
    except Exception as e:
        print(f"An error occurred while reading the CSV file: {e}")
        print("Please ensure the file is a valid CSV and has at least 4 columns.")
        return None

    print("Data loaded successfully! Here's a glimpse:")
    print(df.head())
    print(f"\nTotal rows: {len(df)}")
    print(f"Columns: {df.columns.tolist()}")
    print(f"Initial data types:\n{df.dtypes}")


    # --- Basic Preprocessing (Vibe Coding: Making sense of the data!) ---

    # Drop any rows with missing essential columns (including timestamp for completeness)
    initial_rows = len(df)
    df.dropna(subset=['user_id', 'product_id', 'rating', 'timestamp'], inplace=True)
    rows_after_na = len(df)
    if initial_rows != rows_after_na:
        print(f"\nDropped {initial_rows - rows_after_na} rows with missing essential data.")

    # Convert rating to numeric (if not already)
    df['rating'] = pd.to_numeric(df['rating'], errors='coerce')
    df.dropna(subset=['rating'], inplace=True) # Drop rows where rating couldn't be converted
    print(f"\nData types after rating conversion:\n{df.dtypes}")

    # Convert timestamp to datetime objects (optional but good practice for time-series analysis)
    # The 'coerce' error handling will turn invalid dates into NaT (Not a Time)
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s', errors='coerce')
    df.dropna(subset=['timestamp'], inplace=True) # Drop rows where timestamp couldn't be converted
    print(f"\nData types after timestamp conversion:\n{df.dtypes}")


    # For large datasets, it's common to only consider users/products with a minimum number of interactions
    # This helps with data sparsity and reduces computation. Let's set a threshold.
    min_interactions_per_user = 5
    min_interactions_per_product = 10

    user_counts = df['user_id'].value_counts()
    products_counts = df['product_id'].value_counts()

    # Filter out users with too few interactions
    filtered_users = user_counts[user_counts >= min_interactions_per_user].index
    df_filtered = df[df['user_id'].isin(filtered_users)]

    # Filter out products with too few interactions (re-calculate counts after user filtering)
    products_counts_after_user_filter = df_filtered['product_id'].value_counts()
    filtered_products = products_counts_after_user_filter[products_counts_after_user_filter >= min_interactions_per_product].index
    df_filtered = df_filtered[df_filtered['product_id'].isin(filtered_products)]


    print(f"\nOriginal records: {len(df)}. Records after filtering sparse users/products: {len(df_filtered)}")
    print(f"Unique users: {df_filtered['user_id'].nunique()}")
    print(f"Unique products: {df_filtered['product_id'].nunique()}")

    return df_filtered

# --- Main execution block ---
if __name__ == "__main__":
    # IMPORTANT: Ensure 'ratings_Electronics (1).csv' is in your 'data' folder
    # or update the path to its exact location.
    # For example, if it's in D:\Datasets as you mentioned:
    # data_file = r'D:\Datasets\ratings_Electronics (1).csv'

    # Assuming you placed it in the 'data' subfolder within your project
    # data_file = 'data/ratings_Electronics(1).csv' # <<<--- VERIFY THIS PATH AND FILENAME
    data_file = r'D:\Datasets\ratings_Electronics (1).csv'

    processed_df = load_and_preprocess_data(data_file)

    if processed_df is not None:
        print("\nPreprocessing complete! Sample of processed data:")
        print(processed_df.head())

        # You might want to save this processed data for later use
        # Ensure the 'data' directory exists if you're saving there
        # import os
        # os.makedirs('data', exist_ok=True) # Uncomment if you need to create the 'data' folder
        
        # Saving the processed data
        processed_df.to_csv('D:/Datasets/processed_ecommerce_data.csv', index=False)
        print("\nProcessed data saved to 'data/processed_ecommerce_data.csv'")