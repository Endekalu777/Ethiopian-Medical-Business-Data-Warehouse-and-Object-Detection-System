import os
import pandas as pd
import psycopg2
from dotenv import load_dotenv
import csv
import io
import logging


log_file_path = 'logging/postgres_log.txt'  # Specify the path where you want to save the log file
logging.basicConfig(
    filename=log_file_path,  # Save logs to the specified file
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def load_environment_variables():
    """Load environment variables from a .env file."""
    load_dotenv()
    env_vars = {
        'dbname': os.getenv('DB_NAME'),
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASSWORD'),
        'host': os.getenv('DB_HOST'),
        'port': os.getenv('DB_PORT')
    }
    logger.info("Environment variables loaded")
    return env_vars

def load_csv_to_postgres(table_name, csv_file_path):
    """Load a CSV file into a PostgreSQL table."""
    conn_params = load_environment_variables()

    try:
        with psycopg2.connect(**conn_params) as conn:
            logger.info(f"Connected to database: {conn_params['dbname']}")

            with conn.cursor() as cursor:
                logger.info(f"Reading CSV file: {csv_file_path}")
                # Read the CSV file
                with open(csv_file_path, 'r', encoding='utf-8') as file:
                    csv_data = file.read()

                # Create a StringIO object
                csv_file = io.StringIO(csv_data)

                logger.info(f"Starting data import for table: {table_name}")
                # Use copy_expert 
                cursor.copy_expert(f"COPY {table_name} FROM STDIN WITH CSV HEADER", csv_file)

                conn.commit()
                logger.info(f"Data loaded successfully from {csv_file_path} into {table_name}")

    except Exception as e:
        logger.error(f"An error occurred while processing {csv_file_path}: {e}")

if __name__ == "__main__":
    csv_files = [
        {"table": "doctorset", "file": "C:\\Program Files\\PostgreSQL\\16\\data\\@DoctorsET_data_cleaned.csv"},
        {"table": "lobelia4cosmetics", "file": "C:\\Program Files\\PostgreSQL\\16\\data\\@lobelia4cosmetics_data_cleaned.csv"},
        {"table": "yetenaweg", "file": "C:\\Program Files\\PostgreSQL\\16\\data\\@yetenaweg_data_cleaned.csv"},
        {"table": "eahci", "file": "C:\\Program Files\\PostgreSQL\\16\\data\\@EAHCI_data_cleaned.csv"},
        {"table": "chemed", "file": "C:\\Program Files\\PostgreSQL\\16\\data\\@CheMed123_data_cleaned.csv"},
    ]
    
    logger.info("Starting CSV import process")
    for csv in csv_files:
        logger.info(f"Processing file: {csv['file']}")
        load_csv_to_postgres(csv["table"], csv["file"])
    logger.info("CSV import process completed")