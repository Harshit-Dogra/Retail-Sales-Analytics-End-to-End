# Retail Sales Streamlit Dashboard

## Overview

This directory contains the interactive Streamlit version of the Retail Sales Analytics dashboard.

The application was developed using **Claude**, supported by prompt engineering and human-guided iteration. The goal was not simply to generate a dashboard, but to explore how effectively AI could translate analytical requirements and design direction into a functional data application.

## Purpose

This dashboard was created as an experiment in **AI-assisted development and automation**.

The objectives were to:

- Explore how far AI can go in building a functional analytical application.
- Practice effective prompt engineering for software development.
- Evaluate the quality of AI-generated dashboard code.
- Use AI to accelerate development while keeping human judgment involved.
- Validate the generated application rather than blindly trusting the output.

## How It Was Built

The development process involved:

1. Exploring the dataset and understanding its structure.
2. Identifying relevant business questions and dashboard requirements.
3. Providing Claude with the dataset structure, requirements, and visual direction.
4. Using prompt engineering to guide the generation of the Streamlit application.
5. Manually configuring the local dataset path.
6. Running and testing the generated application.
7. Iterating on the dashboard based on the observed results.
8. Independently validating dashboard calculations using SQL.

The initial dashboard implementation was generated within **minutes**, demonstrating how quickly AI can accelerate application development when provided with clear requirements and direction.

## Features

The dashboard includes:

- Interactive KPI cards
- Dynamic filters
- Monthly revenue trend
- Moving-average analysis
- Payment-method analysis
- Category performance
- Top-performing items
- Top customers
- Dynamic key insights
- Interactive Plotly visualizations
- Previous-period KPI comparisons

## Tech Stack

- **Python**
- **Pandas**
- **Streamlit**
- **Plotly**
- **Claude**

## Running the Application

Install the required dependencies and make sure the dataset path configured in `app.py` points to the local dataset.

Run the application with:

```bash
streamlit run app.py