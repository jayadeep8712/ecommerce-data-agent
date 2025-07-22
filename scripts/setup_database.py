import pandas as pd
import sqlite3
import os

# Define paths
DATA_DIR = '../data'
DB_PATH = '../ecommerce_data.db'
TABLE_NAMES = {
    'product_ad_sales.csv': 'ad_sales',
    'product_total_sales.csv': 'total_sales',
    'product_eligibility.csv': 'eligibility'
}

# Clean up old database if it exists
if os.path.exists(DB_PATH):
    os.remove(DB_PATH)

# Create a connection to the SQLite database
conn = sqlite3.connect(DB_PATH)

# Loop through the CSV files and import them into SQL tables
for csv_file, table_name in TABLE_NAMES.items():
    csv_path = os.path.join(DATA_DIR, csv_file)
    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
        # Clean column names (remove spaces, convert to lowercase)
        df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
        df.to_sql(table_name, conn, if_exists='replace', index=False)
        print(f"Table '{table_name}' created successfully from '{csv_file}'.")
    else:
        print(f"Warning: '{csv_file}' not found in '{DATA_DIR}'.")

# Close the connection
conn.close()

print(f"\nDatabase '{os.path.basename(DB_PATH)}' created and populated.")