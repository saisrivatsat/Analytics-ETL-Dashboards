# Global Insights Through Data: ETL Pipelines and Interactive Dashboards

## 1. Introduction

In the era of open data, integrating information from diverse domains is critical to understanding global challenges. This project implements a modular **Extract–Transform–Load (ETL) pipeline** and develops **interactive dashboards** to analyze three interconnected aspects of society:

* **Air Quality** – Environmental sustainability and urban health indicators, using semi-structured JSON data from the OpenAQ API.
* **World Happiness** – Well-being and life satisfaction trends, using structured survey-based data from Kaggle.
* **Global Unemployment** – Labor market disparities, using structured demographic unemployment data from Kaggle.

The central objective of this work is to design a **reproducible data processing and visualization framework** that combines raw heterogeneous data into relational storage (PostgreSQL) and presents insights through **Streamlit dashboards**.

---

## 2. Objectives

The project aims to:

1. Demonstrate a **modular ETL architecture** capable of processing both structured and semi-structured data.
2. Integrate diverse datasets into a **PostgreSQL database** for unified analysis.
3. Build **interactive dashboards** to make insights accessible and exploratory.
4. Highlight **key findings** across environment, well-being, and economic stability.

---

## 3. Methodology

### 3.1 ETL Pipeline Architecture

The architecture follows a clear progression:

**Extract → Transform → Load → Visualize**

* **Extract**:

  * Air Quality: JSON API requests to OpenAQ.
  * Happiness & Unemployment: CSV datasets from Kaggle.

* **Transform**:

  * Cleaning missing values and inconsistent formats.
  * Normalizing JSON structures into relational tables.
  * Reshaping wide-format unemployment data into long-format time series.

* **Load**:

  * Data inserted into PostgreSQL using parameterized queries (via psycopg2).

* **Visualize**:

  * Dashboards developed in Streamlit, with interactive charts using Plotly and Seaborn.

---

### 3.2 Project Components

#### Air Quality Project

* **Source**: OpenAQ API (semi-structured JSON).
* **Scripts**:

  * `fetch_openaq.py` → API retrieval.
  * `process_pm25.py` → Cleaning and unit standardization.
  * `insert_to_mongodb.py` / `migrate_mongo_to_postgres.py` → Intermediate and final storage.
  * `analyze_and_visualize.py` → Generation of pollutant trend charts.
* **Outputs**: Seasonal PM2.5 plots, top polluted cities, weekday patterns.

#### World Happiness Project

* **Source**: Kaggle dataset (structured CSV).
* **Scripts**:

  * `process_happiness.py` → Handling missing values and standardizing fields.
  * `load_to_postgres.py` → Database integration.
  * `analyze_and_visualize.py` → Correlation analysis and visualizations.
* **Outputs**: GDP vs happiness, corruption vs well-being, top 10 happiest countries.

#### Global Unemployment Project

* **Source**: Kaggle dataset (structured CSV).
* **Scripts**:

  * `process_unemployment.py` → Transformation from wide → long format.
  * `load_to_postgres.py` → Insert into relational schema.
  * `analyze_and_visualize.py` → Segmentation by gender, age, and region.
* **Outputs**: Global unemployment trends, gender gap analysis, youth unemployment spikes.

---

## 4. Repository Structure

```
Analytics-ETL-Dashboards/
│
├── air-quality-project/
│   ├── data/ (raw + cleaned)
│   ├── outputs/ (visualizations)
│   └── src/ (ETL + visualization scripts)
│
├── World-Happiness/
│   ├── data/ (raw + cleaned)
│   ├── outputs/ (visualizations)
│   └── src/
│
├── Global-Unemployment/
│   ├── data/ (raw + cleaned)
│   ├── outputs/ (visualizations)
│   └── src/
│
├── streamlit_dashboard.py (combined dashboard)
├── requirements.txt
└── README.md
```

## Setup

Install dependencies from the consolidated requirements file and launch the unified Streamlit interface:

```bash
pip install -r requirements.txt
streamlit run streamlit_dashboard.py
```

Use the sidebar to switch between the Air Quality, World Happiness, and Global Unemployment dashboards.


Launch the unified Streamlit interface to switch between all dashboards with:

```bash
streamlit run streamlit_dashboard.py
```


---

## 5. Results and Visualizations

### Air Quality

* Seasonal peaks of PM2.5 in urban centers (Delhi, Beijing, Lahore).
* Weekday vs weekend pollutant trends.
* Top 10 polluted cities analysis.

### Happiness

* Strong correlation of happiness with GDP, social support, and life expectancy.
* Negative relationship between perceived corruption and life satisfaction.
* Pandemic-related dips in global well-being (2020–2021).

### Unemployment

* Persistent gender gaps (female > male unemployment rates).
* High youth unemployment rates (>25% in regions like Sub-Saharan Africa).
* Long-term national patterns, e.g., South Africa’s consistently high rates.

---

## 6. Technologies Used

* **Programming**: Python (pandas, numpy, seaborn, matplotlib, plotly)
* **Databases**: PostgreSQL, MongoDB (intermediate store)
* **APIs**: OpenAQ API
* **Visualization**: Streamlit dashboards
* **Data Handling**: psycopg2 for DB integration

---

## 7. Conclusions

This project demonstrates the feasibility and utility of an **integrated ETL pipeline** to process diverse datasets and present insights in a user-friendly, interactive manner. By covering environmental, social, and economic dimensions, it emphasizes how multi-domain data integration can support informed decision-making for policymakers, researchers, and the public.

---

## 8. Future Work

* **Machine Learning Integration** → forecasting air pollution, predicting unemployment, clustering happiness determinants.
* **Geospatial Mapping** → choropleth maps of pollution and unemployment.
* **Deployment Enhancements** → Docker containerization, cloud deployment for dashboards.
* **Additional Datasets** → education, healthcare, or climate indicators.


---

## 9. Contributor

* **Sai Srivatsa Thangallapelly** – Designed and implemented the full ETL pipelines, PostgreSQL integration, and Streamlit dashboards.

