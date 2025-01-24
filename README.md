# Predicting Store Turnover by Time Series Approach

This project aims to predict daily store turnover using a combination of time series analysis and machine learning techniques. Using three years of daily turnover data from 500 stores, combined with store-specific characteristics and weather conditions, we developed and evaluated three predictive models. This study emphasizes the importance of external factors and hybrid model designs in retail analytics.

---

## Table of Contents
- [Overview](#overview)
- [Objectives](#objectives)
- [Technologies Used](#technologies-used)
- [Data](#data)
- [Methodology](#methodology)
- [Models Implemented](#models-implemented)
- [How to Run](#how-to-run)
- [Contributors](#contributors)

---

## Overview
The retail industry faces challenges in accurately predicting sales, directly impacting inventory management, staffing, and marketing strategies. This project leverages state-of-the-art machine learning models to enhance turnover predictions.  

Key features:
- Analysis of turnover data from 500 stores over a 3-year period.
- Forecasting daily store turnover for a two-week horizon.
- Hybrid models combining Long Short-Term Memory (LSTM), Bidirectional LSTM (Bi-LSTM), and Random Forest.

---

## Objectives
The main objectives of this project are:
1. **Model Development and Comparison:** 
   - Implement and evaluate LSTM-Random Forest, BiLSTM-Random Forest ensembles, and standalone Random Forest models.
2. **Feature Integration:** 
   - Incorporate store-specific characteristics and weather data to improve forecasting accuracy.
3. **Prediction Accuracy:** 
   - Minimize prediction errors using advanced techniques and assess models using metrics such as RMSE and MAE.
4. **User Interface:** 
   - Develop a Django-based web application for easy data input, model interaction, and visualization.
5. **Scalability:** 
   - Demonstrate model applicability across various store environments.

---

## Technologies Used
- **Programming Language:** Python 3.12.2
- **Web Framework:** Django 5.1.3
- **Libraries:**
  - Pandas, NumPy: Data preprocessing and manipulation.
  - TensorFlow/Keras: LSTM and BiLSTM implementation.
  - Scikit-learn: Random Forest modeling and metrics.
  - Matplotlib/Seaborn: Visualizations.

---

## Data
The dataset includes:
- **Turnover Data:** Daily sales for 500 stores over three years.
- **Store Features:** Metadata about each store (e.g., type, size, location).
- **Weather Data:** Factors like temperature, precipitation, and special weather events.

---

## Methodology
1. **Data Preprocessing:**
   - Handled missing values, normalized datasets, and engineered temporal features.
2. **Feature Engineering:**
   - Incorporated day of the week, seasonality, and lag features for historical context.
3. **Model Training:**
   - Used a rolling window approach for time series validation.
   - Optimized hyperparameters through grid search and early stopping.
4. **Evaluation:**
   - Metrics: RMSE, MAE, MAPE.
5. **Interface Development:**
   - Implemented forms for data input and results visualization using Django.

---

## Models Implemented
- **LSTM-Random Forest Ensemble:** Combines deep learning and ensemble learning for sequential data.
- **BiLSTM-Random Forest Ensemble:** Adds bidirectional context for improved accuracy.
- **Random Forest:** A standalone model for non-linear relationships and feature interaction analysis.

---

## How to Run
1. **Clone the Repository:**
   ```bash
   git clone https://github.com/sezakocadere/timeseries_turnover.git
   cd timeseries_turnover


---


2. **Run the Django Server:**
   ```bash
   python manage.py runserver

---

## Contributors
- [Seza Kocadere](https://www.linkedin.com/in/sezakocadere/)
- [Marbell Palechor Alarcon](https://www.linkedin.com/in/marbellpalechoralarcon/)
- Miguel Lopez Bustamante
- [Nikhil Kumar Mettapally](https://www.linkedin.com/in/nikhil-mettapally/)
