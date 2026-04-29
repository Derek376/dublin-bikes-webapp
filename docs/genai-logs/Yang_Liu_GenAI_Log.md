# GenAI Log - Yang Liu

## Project
COMP30830 Software Engineering - Dublin Bikes Occupancy and Weather Web Application with Machine Learning Prediction

## Student
Yang Liu

## Role in the Project
My main contribution areas were project setup, data scraping, database design, modular backend structure, data persistence, authentication/favourites support, backend testing, EC2 verification, and final project documentation support. These areas correspond to the backlog tasks assigned to me, including repository setup, team workflow, API research, scraper implementation, MySQL schema design, modularisation of the Flask application, database helper functions, persistence of station and weather data, authentication and favourites implementation, backend tests, EC2 deployment verification, README refinement, final bug fixes, and demo preparation.

## Overview of GenAI Use
GenAI was used as a supporting tool during the project for planning, technical explanation, debugging, documentation, and report wording improvement. It was not used as a replacement for implementation work. All AI-generated suggestions were reviewed, adapted, tested, and aligned with the actual project code, backlog, database design, and deployed application before being used.

---

## Entry 1: Project Setup and Repository Structure

**Related backlog tasks:**
- Create GitHub repository and base project structure
- Define team workflow, branching strategy, and communication channel
- Separate routes, services, templates, and static assets

**Prompt used:**
> We are building a Flask web application for Dublin Bikes using APIs, MySQL, frontend JavaScript, machine learning, and tests. What is a clean project structure for a maintainable coursework project?

**AI output summary:**
The AI suggested separating the application into clear folders for routes, services, templates, static files, database helpers, scraper scripts, machine learning assets, tests, and documentation. It also recommended using a modular Flask structure so that API routes, authentication routes, and database-related logic would not be mixed into a single file.

**How the output was used:**
I used this advice as a reference when organising the repository and separating responsibilities across the project. The final project structure included dedicated areas for Flask routes, service functions, static frontend assets, templates, scraper utilities, machine learning files, tests, and documentation.

**Human review and modification:**
The suggested structure was adapted to match our actual coursework needs and implementation timeline. I only kept the parts that made sense for our app and adjusted the structure based on how our team divided backend, scraper, ML, frontend, and documentation tasks.

---

## Entry 2: JCDecaux and OpenWeather API Research

**Related backlog tasks:**
- Research JCDecaux and OpenWeather API structures
- Implement first version of bike and weather scrapers

**Prompt used:**
> Explain how to design a Python scraper that collects Dublin Bikes station data from the JCDecaux API and weather data from OpenWeather, then prepares the data for storing in MySQL.

**AI output summary:**
The AI explained that the scraper should separate API fetching, response validation, field extraction, database insertion, and error handling. It also suggested storing bike station data and weather data in separate tables because they have different structures and update frequencies.

**How the output was used:**
I used the response to think through the scraper workflow and the relationship between external API data and database storage. The scraper implementation was structured around collecting station availability data, collecting weather data, and storing those values for later backend retrieval.

**Human review and modification:**
The API field names, request parameters, and database insertion logic were checked against the actual JCDecaux and OpenWeather responses. The final code was implemented and tested against our real API keys and local/EC2 environment rather than copied directly from AI output.

---

## Entry 3: MySQL Database Design

**Related backlog tasks:**
- Design MySQL schema for stations, weather, users, and favourites
- Implement table creation script and database connection helpers
- Persist station history records in MySQL
- Persist current, hourly, and daily weather data in MySQL

**Prompt used:**
> Help me design a MySQL schema for a Dublin Bikes web app that stores station data, station availability history, current weather, hourly forecast, daily forecast, users, and favourite stations.

**AI output summary:**
The AI recommended separating current station metadata, historical station observations, weather records, users, and favourites into different tables. It also suggested that the favourites table should act as a linking table between users and stations.

**How the output was used:**
This helped shape the database design rationale. The schema was organised around logical data areas: station data, historical availability data, weather data, user accounts, and user favourites. This supported the map display, historical queries, weather panel, authentication, and personalised favourite stations.

**Human review and modification:**
The final database design was matched to our real Flask routes and service-layer functions. The weather tables were treated as city-level context rather than station-specific records, and the favourites relationship was implemented according to the actual login and station workflow used in the app.

---

## Entry 4: Authentication and Favourites Feature Support

**Related backlog tasks:**
- Implement user registration and login routes
- Implement logout and auth status handling
- Implement favourites table and API operations

**Prompt used:**
> What backend routes and service functions are needed for login, logout, registration, and favourite station management in a Flask application?

**AI output summary:**
The AI suggested separating authentication routes from service logic, using session-aware state changes, validating user inputs, hashing or securely storing passwords, and creating API endpoints for adding, removing, and listing favourite stations.

**How the output was used:**
The response helped confirm that authentication and favourites should be handled as separate backend concerns instead of being mixed directly into map or station routes. The final implementation included routes and service logic for user registration, login, logout, checking authentication state, and managing favourite stations.

**Human review and modification:**
The final behaviour was manually integrated with our frontend UI and database schema. The favourites feature was tested in combination with login state because it depended on both authenticated users and station selection.

---

## Entry 5: Backend Testing and Pytest Debugging

**Related backlog tasks:**
- Write and run backend tests
- Verify local app integration with database-backed APIs

**Prompt used:**
> How should I test Flask routes for authentication, favourites, station data, weather data, and prediction using pytest and Flask test client?

**AI output summary:**
The AI suggested using Flask's test client to simulate requests, checking response status codes and JSON outputs, and using mocks for external API or database-dependent behaviour where appropriate. It also recommended testing both successful and failure cases.

**How the output was used:**
I used this guidance to support the backend test strategy. The test suite covered app setup, authentication, favourites operations, data routes, and prediction-related behaviour. Tests were run locally before final submission.

**Human review and modification:**
The tests were adapted to match our actual route names, response structures, session behaviour, and fallback logic. When one prediction test expected an error for missing weather data but the backend correctly returned a successful fallback response, the test expectation was updated to reflect the implemented design.

---

## Entry 6: EC2 Deployment and Model Stability

**Related backlog tasks:**
- Deploy and verify app on EC2
- Refine README, final bug fixes, and demo preparation

**Prompt used:**
> Our Flask application with a Random Forest model is deployed on AWS EC2, but loading the model may cause memory issues. What should we check and how can we make the deployment more stable?

**AI output summary:**
The AI suggested checking memory usage, reducing the model size, using joblib compression, limiting tree complexity, avoiding unnecessary repeated model loading, and ensuring the Flask app uses stable production settings where possible.

**How the output was used:**
This supported our deployment optimisation work. The model was pruned and compressed to reduce memory usage, and the deployment was verified on EC2. This helped make the prediction endpoint more stable for the final demo.

**Human review and modification:**
The final solution was based on actual EC2 behaviour and testing. The optimisation was not accepted blindly; it was validated by checking that the application still loaded, the prediction endpoint worked, and the model performance remained acceptable.

---

## Entry 7: Report and Documentation Support

**Related backlog tasks:**
- Refine README, final bug fixes, and demo preparation
- Support final report documentation

**Prompt used:**
> Help me explain the backend architecture, database design rationale, testing strategy, and sprint process for a Flask-based Dublin Bikes web application report.

**AI output summary:**
The AI suggested writing the report around separation of concerns, modular Flask routes and services, database design choices, testing evidence, sprint reviews, sprint retrospectives, and EC2 deployment.

**How the output was used:**
I used the response to improve documentation clarity and make sure the report explained not only what was implemented, but also why the design choices were made. This supported sections on architecture, database design, testing, process, and final deployment.

**Human review and modification:**
The final report wording was edited to match the real application, backlog workbook, test results, and project diagrams. AI suggestions were treated as drafting support rather than final evidence.

---

## Reflection
GenAI was useful for accelerating planning, clarifying technical options, debugging test expectations, and improving report explanations. However, it was only used as a support tool. The project code, database design, tests, deployment configuration, and report content were checked against the real application and backlog before submission. Any AI-generated advice that did not match the actual implementation was modified or rejected.
