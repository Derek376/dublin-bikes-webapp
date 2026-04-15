# 🚲 Dublin Bikes Web Application

**Dublin Bikes Web Application** is a Flask-based web system for displaying real-time and historical Dublin Bikes station occupancy and weather information, with machine learning-based bike availability prediction. The project was developed as part of the **COMP30830** course and follows a Scrum-based team workflow. It combines **Flask**, **JavaScript**, **MySQL**, **external APIs**, and **Scikit-learn** to deliver an interactive bike-sharing information platform.

---

## 📋 Table of Contents

- [✨ Features](#-features)
- [🏗️ Project Structure](#️-project-structure)
- [🚀 Getting Started](#-getting-started)
  - [🔧 Installation](#-installation)
  - [⚙️ Configuration](#️-configuration)
  - [🗄️ Database Setup](#️-database-setup)
  - [📥 Running the Scraper](#-running-the-scraper)
  - [🤖 ML Model Setup](#-ml-model-setup)
- [💻 Usage](#-usage)
- [🤖 Machine Learning Model](#-machine-learning-model)
- [🧪 Testing](#-testing)
- [📂 API Overview](#-api-overview)
- [🤝 Team Workflow](#-team-workflow)
- [📝 License](#-license)

---

## ✨ Features

- **📍 Interactive station map**  
  Display Dublin Bikes stations on a visual map with live occupancy and availability information.

- **🌦️ Weather integration**  
  Show current weather and forecast data alongside bike station information.

- **📊 Historical station trends**  
  Retrieve and display historical station occupancy data from the database.

- **🔄 Data collection pipeline**  
  Collect real-time data from **JCDecaux API** and weather data from **OpenWeather API**, then store them in MySQL.

- **🤖 ML-based occupancy prediction**  
  Predict bike availability using a trained machine learning model based on historical and weather-related features.

- **🔐 User authentication**  
  Register, log in, and manage a personal account.

- **⭐ Favorites feature**  
  Save favorite bike stations for quick access.

---

## 🏗️ Project Structure

```bash
dublin-bikes-webapp/
│
├── app/                    # Main Flask application
│   ├── routes/             # Route blueprints (live API, DB API, auth, favorites, pages)
│   ├── services/           # Business logic, DB access, external API helpers
│   ├── static/             # CSS, JavaScript, images
│   ├── templates/          # HTML templates
│   └── __init__.py
│
├── config/                 # App/database configuration
├── scraper/                # Data collection scripts and DB table creation
├── ml/                     # ML training notebook and trained model file
├── tests/                  # Automated tests
├── docs/                   # Personas, user stories, mockups, acceptance criteria, etc.
├── requirements.txt        # Python dependencies
├── run.py                  # App entry point
└── README.md
```

---

## 🚀 Getting Started

### 🔧 Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/Derek376/dublin-bikes-webapp.git
   ```

2. Move into the project folder:

   ```bash
   cd dublin-bikes-webapp
   ```

3. Create the Conda environment:

   ```bash
   conda env create -n dublin-bikes-env -f environment.yml
   ```

4. Activate the Conda environment:
   ```bash
   conda activate dublin-bikes-env
   ```

---

### ⚙️ Configuration

1. Copy `.env.example` to a new file named `.env`.

2. Open the `.env` file.

3. Replace the placeholder values with your own configuration details and API keys.

---

### 🗄️ Database Setup

Before running the application, create the MySQL database and required tables.

1. Create the database manually in MySQL:

   ```sql
   CREATE DATABASE comp30830_bikes;
   ```

2. Run the table creation script:
   ```bash
   python scraper/create_tables.py
   ```

This will create the tables needed for:

- station metadata
- bike availability history
- weather data
- users
- favorites

You can also change the database name, but don't forget to update the `.env` file accordingly.

---

### 📥 Running the Scraper

To collect and store live station and weather data:

```bash
python -m scraper.run_scraper
```

This scraper fetches:

- station occupancy data from **JCDecaux**
- weather data from **OpenWeather**

and stores them in the local MySQL database for later retrieval and analysis.

---

### 🤖 ML Model Setup

Before starting the Flask application, make sure the trained model file has been generated.

The trained model file is not included in the repository because of file size limits.
To generate it locally, run `model_training.ipynb` in the `ml/` directory.

The prediction feature depends on this file, and the application may not start correctly without it.

---

### Dataset note

The merged dataset file `ml/final_merged_data.csv` is not included in the repository because it exceeds GitHub's file size limit.

It is used during the machine learning workflow in the `ml/` directory and can be regenerated locally through the data preparation and model training process if needed.

## 💻 Usage

### Start the Flask application

```bash
python run.py
```

Then open your browser and go to:

```bash
http://127.0.0.1:5000
```

### Main supported functionality

- View all Dublin Bikes stations on the map
- Click a station to see availability details
- View weather information
- View historical station trends
- Register / log in
- Add favorite stations
- Request ML-based occupancy predictions

---

## 🤖 Machine Learning Model

The project includes a machine learning model trained on historical bike occupancy and weather-related features.

### ML workflow

- Clean and preprocess historical data
- Select features relevant to bike occupancy
- Train multiple models
- Compare performance
- Save the best-performing model for app usage

### Model file

The Flask app expects a trained model file such as:

```bash
ml/best_bike_model.joblib
```

---

## 🧪 Testing

To run the automated tests from the project root directory:

```bash
python -m pytest -q
```

The tests are located in the `tests/` directory and verify core backend routes and key application behavior.

Current test coverage includes:

- homepage and health routes
- live API routes
- database API routes
- authentication validation
- favorites access control
- prediction endpoint validation and success cases

---

## 📂 API Overview

### Live API routes

- `/api/live/jcdecaux`
- `/api/live/weather/current`
- `/api/live/weather/hourly`
- `/api/live/weather/daily`

### Database API routes

- `/api/db/stations`
- `/api/db/stations/<station_number>`
- `/api/db/stations/<station_number>/history?limit=50`
- `/api/db/weather/current`
- `/api/db/weather/hourly?limit=24`
- `/api/db/weather/daily?limit=16`
- `/api/db/predict`

### Auth routes

- `/auth/register`
- `/auth/login`
- `/auth/logout`
- `/auth/me`

### Favorites routes

- `/api/favorites`
- `/api/favorites/<station_number>`
- `/api/favorites/<station_number>/status`

---

## 🤝 Team Workflow

This project was developed using **Scrum**, with sprint-based planning and implementation.

### Sprint focus

- **Sprint 1**: requirements, user stories, mockups, setup, initial scraping
- **Sprint 2**: scraping, Flask backend, preliminary frontend
- **Sprint 3**: frontend refinement and optional features
- **Sprint 4**: machine learning model and testing

The final stage focused on:

- refactoring
- polishing the UI and codebase
- preparing the report
- improving documentation
- preparing the demo video

---

## 📝 License

This project is licensed under the **MIT License**.  
See the [LICENSE](LICENSE) file for more details.

---

## 🧑‍💻 Made with ❤️ by

- [Derek](https://github.com/Derek376)
- [Henry](https://github.com/flackothegoat)
- [Jason](https://github.com/eelj457)

Happy coding! 🚀
