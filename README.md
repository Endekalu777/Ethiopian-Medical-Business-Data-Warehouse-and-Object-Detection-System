# Ethiopian Medical Business Data Scraping and API Development

This project focuses on scraping data from specific Telegram channels related to Ethiopian medical businesses and deploying an API for object detection using YOLO. The goal is to automate data collection, clean and process the data, and perform object detection on images collected from these channels.

## Project Overview

The main objective is to collect, clean, and process data related to Ethiopian medical businesses, followed by implementing object detection on the images using the YOLO algorithm. The project is divided into several tasks:

### Key Tasks
1. **Data Scraping and Collection** from Telegram channels.
2. **Data Cleaning and Transformation** using DBT (Data Build Tool).
3. **Object Detection** on medical-related images using YOLO.
4. **API Development and Deployment** using FastAPI to serve object detection results.

## Installation

### Creating a Virtual Environment

#### Using Conda

If you prefer Conda as your package manager:

1. Open your terminal or command prompt.
2. Navigate to your project directory.
3. Run the following command to create a new Conda environment:

    ```bash
    conda create --name medical_scraping_api python=3.12.5
    ```

4. Activate the environment:

    ```bash
    conda activate medical_scraping_api
    ```

#### Using Virtualenv

If you prefer using `venv`, Python's built-in virtual environment module:

1. Open your terminal or command prompt.
2. Navigate to your project directory.
3. Run the following command to create a new virtual environment:

    ```bash
    python -m venv medical_scraping_api
    ```

4. Activate the environment:

    - On Windows:
        ```bash
        .\medical_scraping_api\Scripts\activate
        ```
    - On macOS/Linux:
        ```bash
        source medical_scraping_api/bin/activate
        ```

### Installing Dependencies

Once your virtual environment is created and activated, install the required dependencies using:

```bash
pip install -r requirements.txt

## Project Structure
Data_Warehouse/
├── dbt_model/
my_project/
├── templates/
│   ├── index.html
│   └── detections.html
├── crud.py
├── database.py
├── main.py
├── models.py
├── schemas.py
notebooks/
├── Object_detection_Yolov5x.ipynb
├── cleaning.ipynb
scripts/
├── __init__.py
├── cleaning.py
├── database_setup.py
├── postgres_script.py
├── telegram_scrapper.py
.gitignore
README.md

## Usage Instructions
- Data Collection
Run scraping_telegram.py to scrape data from Telegram channels and store them in a structured format.
- Data Cleaning
Use the data_cleaning.py script to clean and transform the collected data using DBT.

 
## API Deployment
Start the FastAPI server by running:

```
uvicorn app.main:app --reload
```
## Contributions
Contributions are welcome! If you find any issues or have suggestions for improvement, feel free to create a pull request or open an issue.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.

## Contact
For any questions or additional information, please contact [Endekalu Simon Haile](mailto:Endekalu.simon.haile@gmail.com).