# Dublin Bikes Web App

Bike sharing web application with:

- station availability map
- weather data
- historical occupancy
- ML-based prediction

Developed for Software Engineering course using Scrum.

---

## Tech Stack

Backend:

- Python
- Flask

Frontend:

- HTML / CSS / JavaScript

Other:

- Web scraping
- MySQL (later)
- Scikit-learn (ML later)

---

## Project Structure

```
dublin-bikes-app/
│
├── app/ # Flask backend (routes, templates, static)
├── scraper/ # Data collection scripts
├── models/ # ML models
├── docs/ # Personas, stories, mockups
├── tests/
├── run.py # App entry point
├── requirements.txt
```

---

## Setup & Run (Windows Git Bash)

### 1. Create virtual environment

python -m venv venv

### 2. Activate

source venv/Scripts/activate

### 3. Install dependencies

pip install -r requirements.txt

### 4. Run Flask

python run.py

### 5. Open browser

http://127.0.0.1:5000

You should see:
"Flask is running ✅"

---

## Sprint 1 Status

Completed:

- Repo setup
- Flask setup
- Personas
- Interviews
- User stories
- Mockups

Next:

- Data scraper
- Map integration
- Database
- ML prediction

---

## Team

- Member A – Yang Liu
- Member B – Yuhao Xu
- Member C – Jason Lee
