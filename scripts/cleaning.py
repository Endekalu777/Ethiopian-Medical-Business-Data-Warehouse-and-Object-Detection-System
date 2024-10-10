import pandas as pd
import logging
from IPython.display import display


logging.basicConfig(filename='data_cleaning.log', level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')

def clean_dataset(file_path):
    logging.info(f"Starting to clean dataset: {file_path}")
    
    # Load the CSV file
    df = pd.read_csv(file_path)
    
    # Log initial shape
    logging.info(f"Initial shape: {df.shape}")
    
    # Remove duplicates
    df = df.drop_duplicates().reset_index(drop=True)
    
    # Drop rows where 'message' or 'media path' are missing
    df = df.dropna(subset=['Message', 'Media Path'])
    
    # Handle missing values for 'views'
    # We'll use the median of non-null values to fill missing views
    median_views = df['views'].median()
    df['views'] = df['views'].fillna(median_views)

    # show missing values after they are handled
    missing_values = df.isnull().sum()
    missing_percentage = (missing_values / len(df)) * 100
    missing_df = pd.DataFrame({'Missing Values': missing_values, 'Percentage': missing_percentage})
    display(missing_df)
    
    # Standardize formats
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df['views'] = df['views'].astype(int)
    
    # Data validation
    df = df[df['views'] >= 0]
    df = df[df['Message'].str.strip() != '']
    
    # Log the number of rows with missing values after cleaning
    missing_values = df.isnull().sum()
    logging.info("Missing values after cleaning:")
    logging.info(missing_values)
    
    # Log final shape
    logging.info(f"Final shape: {df.shape}")
    
    # Save cleaned data
    cleaned_file_path = file_path.replace('.csv', '_cleaned.csv')
    df.to_csv(cleaned_file_path, index=False)
    
    logging.info(f"Finished cleaning dataset: {file_path}")
    logging.info(f"Cleaned data saved to: {cleaned_file_path}")
    
    return cleaned_file_path