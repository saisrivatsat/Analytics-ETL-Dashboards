

# Air Quality (PM2.5) Analysis Project

## Overview
This project fetches, processes, and analyzes PM2.5 air quality data from the OpenAQ API. It transforms semi-structured JSON data into a structured format, enriches it with geolocation information, stores it in databases (MongoDB and PostgreSQL), and provides visualizations and an interactive dashboard to explore the data.

### Objectives
- Collect PM2.5 data from OpenAQ API.
- Store raw data in MongoDB and processed data in PostgreSQL.
- Enrich data with city and country information using reverse geocoding.
- Analyze trends and distributions of PM2.5 levels over time and location.
- Generate visualizations and an interactive Streamlit dashboard.

## Project Structure
- **data/**
  - **raw/**: Raw PM2.5 data (`pm25_daily_full.csv`, `pm25_daily_full.json`).
  - **processed/**: Enriched data (`pm25_geo_enriched.csv`).
- **outputs/**: Visualizations (e.g., `daily_pm25_trend.png`, `top10_cities_pm25.png`).
- **src/**: Python scripts for the pipeline.
- `.env`: Environment file for API key.
- `logfile.log`: Logs for debugging.
- `requirements.txt`: Dependencies for the project.
- `README.md`: This documentation.

## Setup Instructions
1. **Clone the Repository**:
   ```bash
   git clone <repository_url>
   cd air-quality-project
   ```

2. **Install Dependencies**:
   Ensure Python 3.8+ is installed, then install required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up Environment**:
   - Create a `.env` file in the project root:
     ```plaintext
     OPENAQ_API_KEY=your_openaq_api_key_here
     ```
   - Obtain an API key from [OpenAQ](https://openaq.org/) and replace `your_openaq_api_key_here`.

4. **Set Up Databases**:
   - **MongoDB**: Ensure MongoDB is running on `localhost:27017`.
     ```bash
     mongod
     ```
   - **PostgreSQL**: Set up a database on `localhost:5433` with user `saisrivatsat`.
     - Create the database:
       ```bash
       createdb airqualitydb
       ```
     - Create the `pm25_data` table:
       ```sql
       psql -h localhost -p 5433 -U saisrivatsat -d airqualitydb
       CREATE TABLE pm25_data (
           id SERIAL PRIMARY KEY,
           date TIMESTAMP,
           pm25 FLOAT,
           sensor_id INTEGER,
           city VARCHAR(255),
           country VARCHAR(255)
       );
       ```

## Execution Order
Run the scripts in the following order from the project root:

1. **Fetch Data**:
   ```bash
   python src/fetch_openaq.py
   ```
   - Fetches PM2.5 data and saves to `data/raw/pm25_daily_full.csv` and `.json`.

2. **Insert into MongoDB**:
   ```bash
   python src/insert_to_mongodb.py
   ```
   - Loads raw JSON data into MongoDB (`airquality.pm25_raw`).

3. **Migrate to PostgreSQL**:
   ```bash
   python src/migrate_mongo_to_postgres.py
   ```
   - Migrates raw data from MongoDB to PostgreSQL (`pm25_data` table).

4. **Process and Enrich Data**:
   ```bash
   python src/process_pm25.py
   ```
   - Cleans data, adds geolocation (city, country, latitude, longitude), and saves to `data/processed/pm25_geo_enriched.csv`.

5. **Load Enriched Data into PostgreSQL**:
   ```bash
   python src/load_enriched_to_postgres.py
   ```
   - Loads enriched data into PostgreSQL (`pm25_data` table).

6. **Analyze and Visualize**:
   ```bash
   python src/analyze_and_visualize.py
   ```
   - Generates visualizations in `outputs/` (e.g., daily trends, top cities, distributions).

7. **Launch Dashboard**:
   ```bash
   streamlit run streamlit_dashboard.py
   ```
   - Opens an interactive dashboard with filters, KPIs, and visualizations.

## Outputs
- **Raw Data**: `data/raw/pm25_daily_full.csv`, `data/raw/pm25_daily_full.json`.
- **Processed Data**: `data/processed/pm25_geo_enriched.csv` (includes date, PM2.5, sensor ID, city, country, latitude, longitude).
- **Visualizations**: In `outputs/`:
  - `daily_pm25_trend.png`: Daily PM2.5 trend.
  - `top10_cities_pm25.png`: Top 10 cities by average PM2.5.
  - `pm25_distribution.png`: Distribution of PM2.5 levels.
  - `country_pm25.png`: Average PM2.5 by country.
  - `monthly_avg_pm25.png`: Monthly PM2.5 trend.
  - `weekday_avg_pm25.png`: Average PM2.5 by day of the week.
  - `yearly_avg_pm25.png`: Yearly PM2.5 trend.
- **Dashboard**: Interactive Streamlit dashboard with filters (country, city, date), KPIs, and visualizations (trends, maps, patterns).

## Notes
- Ensure the OpenAQ API key is valid to avoid fetch failures.
- Nominatim geocoding has rate limits; the script includes delays to comply.
- Check `logfile.log` for debugging if errors occur.
- PM2.5 values are clipped to 0–500 µg/m³ to handle outliers.

## Troubleshooting
- **API Errors**: Verify the `OPENAQ_API_KEY` in `.env`.
- **Database Connection Issues**: Ensure MongoDB and PostgreSQL are running and configured correctly.
- **Geocoding Failures**: Increase `time.sleep` in `process_pm25.py` if rate limits are hit.

