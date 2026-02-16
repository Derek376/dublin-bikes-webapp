# System Features

This document defines the high-level functional features of the Dublin Bikes Web Application.

The system aims to provide real-time station information, historical data insights, and predictive analysis to support users of the Dublin bike-sharing system.

---

## 1. Station Map System

The system shall:

- Display all Dublin bike stations on an interactive Google Map.
- Show real-time availability (number of available bikes and free stands).
- Allow users to click on station markers to view detailed information.
- Automatically refresh station data at regular intervals.

---

## 2. Data Collection and Storage

The system shall:

- Collect station data from the JCDecaux API.
- Store historical station availability data in a database.
- Collect weather data from a public weather API.
- Store weather data for analysis and prediction.
- Support automated periodic data updates.

---

## 3. Historical Data Visualization

The system shall:

- Allow users to view historical occupancy data for a selected station.
- Display data in graphical format (e.g., charts).
- Provide hourly and daily trends.
- Allow users to select a time range for visualization.

---

## 4. Weather Integration

The system shall:

- Display current weather information.
- Show basic weather indicators such as temperature and conditions.
- Enable analysis of the relationship between weather and bike availability.

---

## 5. Machine Learning Prediction

The system shall:

- Train a prediction model using historical station and weather data.
- Predict future bike availability for a selected station.
- Allow users to select date and time for prediction.
- Display prediction results clearly in the interface.

---

## 6. User Interaction and Interface

The system shall:

- Provide a simple and intuitive user interface.
- Support interactive map navigation.
- Handle user input validation.
- Ensure clear navigation between main pages.

---

## 7. Optional Enhancement (Additional Feature)

The system may additionally support one enhancement feature, such as:

- Journey planning between stations.
- Station recommendation system.
- Peak time alerts.
- User account or subscription management.
