# Retail Sales Analytics: End-to-End Data Analytics Project

## Project Overview

This project demonstrates a complete end-to-end data analytics workflow, transforming raw retail sales data into actionable insights through deliberate, reasoned decision-making at every stage of the pipeline.

The analysis covers a three-year period (2022–2024), encompassing approximately 1.53M in total revenue generated from 11.7K unique orders and over 65K items sold. The project follows a structured pipeline involving data inspection, cleaning, exploratory data analysis, and business reporting.

---

## Data Source

Dataset: [Retail Store Sales: Dirty for Data Cleaning](https://www.kaggle.com/datasets/ahmedmohamed2003/retail-store-sales-dirty-for-data-cleaning)

Note: This is a synthetic dataset designed to simulate real-world retail sales data, including intentional inconsistencies for data cleaning practice. As the dataset does not specify a country or region, currency values are represented as numeric figures without a currency symbol.

---

## Data Considerations

The original dataset contained records from 2022 to 2025. However, the 2025 data only covered the period up to January 18, resulting in an incomplete year.

To maintain analytical integrity:

* The partial 2025 records were excluded from temporal analysis during EDA.
* The 2025 data was completely removed from the Power BI model to maintain reporting consistency.
* Final trend analysis and dashboard reporting were therefore based on complete yearly data from 2022 to 2024.

---

## Technologies Used

* **Data Inspection:** Microsoft Excel
* **Programming Language:** Python
* **Libraries:** Pandas, NumPy, Matplotlib, Seaborn
* **Development Environment:** Jupyter Notebook
* **Business Intelligence & Reporting:** Power BI
* **Data Modeling & Measures:** DAX

---

## Analytics Pipeline

### Excel – Data Inspection

Initial data validation was performed in Excel to understand the dataset structure before any transformation.

Tasks included:

* Inspecting columns and data types.
* Checking for missing values.
* Identifying duplicate records.
* Understanding the overall dataset composition.

### Python (Jupyter Notebook) – Data Cleaning & Exploratory Data Analysis

Two separate notebooks were created:

#### 1. Data Validation and Cleaning

The dataset contained 12,575 rows and 11 columns. Rather than applying a default drop strategy — which would have reduced the dataset to approximately 7,000 rows — a deliberate, column-by-column cleaning approach was followed:

* **Discount Applied** (4,199 missing values) — Filled with "Unknown" as a data preservation technique. This placeholder was intentionally excluded from final analysis and dashboard reporting, as the equal ~1/3 distribution across True, False, and Unknown indicated no meaningful signal.
* **Item** (1,213 missing values) — Column dropped entirely as it held no analytical value.
* **Price Per Unit** (609 missing values) — Recovered using the mathematical relationship: Total Spent = Price Per Unit × Quantity. Where both Quantity and Total Spent were present, Price Per Unit was calculated accordingly.
* **Quantity & Total Spent** (604 missing values each) — Both columns were simultaneously missing in the same 604 records, making mathematical recovery impossible. These records were dropped to maintain data reliability.
* **Transaction Date** — Converted from string to datetime format to enable accurate time-series analysis.

Duplicate records were also checked — no duplicates were found, confirming the uniqueness and integrity of each transaction record.

* Original Dataset: 12,575 rows
* Cleaned Dataset: 11,971 rows

#### 2. Exploratory Data Analysis (EDA)

Business questions were addressed through Univariate, Bivariate, and Multivariate analysis, focusing on:

* Sales patterns and revenue trends.
* Category performance and Average Order Value.
* Customer purchasing behavior.
* Payment method preferences.

### Power BI – Interactive Dashboard and Reporting

A corporate-style interactive dashboard was developed to provide stakeholders with a clean, high-level view of business performance.

The dashboard enables:

* Monitoring revenue trends over time.
* Evaluating product category performance.
* Comparing Average Order Values across categories.
* Analyzing payment method contributions.
* Understanding transaction distribution and customer preferences.

> Dashboard screenshots available in the `/screenshots` folder.

---

## Key Insights

### Seasonal Revenue Pattern
Revenue consistently peaks during December–January across all three years, indicating a recurring seasonal demand pattern likely aligned with festive periods. This pattern is validated by the 3-year average, making it a reliable business insight rather than a one-time anomaly.

### Category Performance
Butchers generated the highest revenue and recorded the highest Average Order Value (AOV) of 138.86, while Milk Products showed the lowest revenue and lowest AOV of 119.32. Overall, category performance remained relatively balanced across all segments.

### Annual Performance
Business performance remained stable across the three-year period, with 2024 recording the highest annual revenue.

### Payment Behavior
Cash was the most frequently used payment method and generated the highest total revenue, contributing approximately 530K in sales. Credit Cards and Digital Wallets also maintained significant shares, indicating diversified payment preferences.

### Order Value Stability
Despite monthly fluctuations in revenue, transaction values remained highly consistent, averaging approximately 129.71 per order.

---

## Conclusion

This project demonstrates that thoughtful data decisions matter as much as technical execution. From recovering missing values mathematically, to excluding incomplete yearly data, to filtering inconclusive variables from the dashboard — every decision was made with analytical integrity and business context in mind.

By combining Excel, Python, and Power BI, this project showcases the complete analytics lifecycle — from raw data inspection to business reporting and insight generation.