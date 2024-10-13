import os
import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, Float 
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import logging

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(filename='data_insertion.log', level=logging.INFO, format='%(asctime)s %(message)s')

# Database configuration from the .env file
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# Create the PostgreSQL connection string
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Set up the database connection
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Define the DetectionResult model (for the detections_yolo table)
class DetectionResult(Base):
    __tablename__ = "detections_yolo" 
    
    id = Column(Integer, primary_key=True, index=True)
    image_name = Column(String, index=True)
    class_name = Column(String, index=True)
    confidence = Column(Float)
    x_min = Column(Float)
    y_min = Column(Float)
    x_max = Column(Float)
    y_max = Column(Float)
    source = Column(String)  

# Create the detections_yolo table if it doesn't exist
Base.metadata.create_all(bind=engine)

# Function to insert detection data into the PostgreSQL database
def insert_detection_data(db, row, source):
    detection = DetectionResult(
        image_name=row['image_name'],    # Adjusted to your column name
        class_name=row['name'],          # Adjusted to your column name
        confidence=row['confidence'],
        x_min=row['xmin'],
        y_min=row['ymin'],
        x_max=row['xmax'],
        y_max=row['ymax'],
        source=source  # Add the source (Chemed or Lobelia)
    )
    db.add(detection)
    db.commit()
    db.refresh(detection)

# Main function to process CSVs and insert data into the database
def process_csv(file_path, source):
    db = SessionLocal()
    
    # Load the CSV file
    df = pd.read_csv(file_path)
    
    # Iterate over CSV rows and insert into the database
    for index, row in df.iterrows():
        try:
            insert_detection_data(db, row, source)
            logging.info(f"Inserted detection for image {row['image_name']} from {source}")
        except Exception as e:
            logging.error(f"Failed to insert detection for image {row['image_name']} from {source}: {e}")
    
    db.close()

# Execute the main function for both Chemed and Lobelia datasets
if __name__ == "__main__":
    chemed_csv = "Chemed_all_detections.csv"  
    process_csv(chemed_csv, "Chemed")

    # Process the Lobelia CSV
    lobelia_csv = "lobelia4cosmetics_all_detections.csv" 
    process_csv(lobelia_csv, "Lobelia4cosmetics")