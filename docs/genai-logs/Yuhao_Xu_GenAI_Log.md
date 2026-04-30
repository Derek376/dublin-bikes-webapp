# GenAI Log - Yuhao Xu

## Project
COMP30830 Software Engineering - Dublin Bikes Occupancy and Weather Web Application with Machine Learning Prediction

## Student
Yuhao Xu

## Role in the Project
My main contribution areas spanned across agile project management assistance, backend API development, the end-to-end machine learning pipeline, and deployment troubleshooting. On the technical side, I implemented the Flask application factory and developed the core API endpoints for live/historical station data and weather data. I led the machine learning module, which included preparing the merged dataset, engineering time and weather features, training and evaluating regression models, and saving the best model file. Finally, I integrated the model loading route into the Flask backend, connected the prediction controls to the frontend display, and assisted in troubleshooting AWS EC2 deployment issues.

## Overview of GenAI Use
Generative AI was utilised strictly as an analytical assistant, debugging tool, and brainstorming partner throughout the project lifecycle. It was primarily used to break down complex project requirements into manageable agile tasks during the initial phase, suggest Python libraries for data analysis, and diagnose server-side memory crashes. I did not use GenAI to generate final project code blindly; all AI suggestions were manually reviewed, rewritten to fit our specific database schema and architectural patterns, and rigorously tested in our local and EC2 environments.

---

## Entry 1: Initial Project Breakdown and Backlog Generation

**Prompt used:**
> I have some project specification documents for a Dublin Bikes web app using Flask, MySQL, APIs, and Machine Learning. Based on this document, can you outline the main development phases and suggest a high-level list of product backlog items for our initial sprint planning?

**AI output summary:**
The AI analysed the provided text and broke the project down into logical phases: Infrastructure Setup, Data Harvesting, Backend Development, Frontend Display, Machine Learning, and Cloud Deployment (without the extra function because we haven't decided yet). It provided a drafted list of epics and associated backlog tasks.

**How the output was used:**
I used this output as a structural foundation during our Sprint 1. Although drafting the initial backlog was formally assigned to another team member (Jason), I used the AI's breakdown to assist the team in ensuring we didn't miss critical milestones like setting up the database connection pool early on.

**Human review and modification:**
The AI's generated backlog was too generic. I manually refined the tasks with the team, assigned specific story points based on our velocity, and reformatted them into proper tracking formats and applied them into Jira. 

---

## Entry 2: Refining User Stories and Acceptance Criteria

**Prompt used:**
> We are defining a User Story for the machine learning feature: 'As a user, I want to request a prediction for a selected station so I can choose my ideal station.' What are some robust and testable Acceptance Criteria for this story?

**AI output summary:**
The AI suggested several technical and user-centric ACs, such as: "Given valid station ID and future time, the system returns a predicted integer," "Given missing time inputs, the UI shows an error message," and "The prediction must use the nearest future weather forecast."

**How the output was used:**
This helped me standardise the formatting of our Acceptance Criteria and ensure edge cases (like invalid user inputs or missing weather data) were explicitly documented before I began developing the prediction features.

**Human review and modification:**
I modified the AI's suggestions to strictly match the UI design our team agreed upon. I removed AI suggestions about "sending email alerts for predictions" as it was out of scope, focusing purely on the frontend UI constraints we actually implemented.

---

## Entry 3: Flask Application Factory and API Endpoints

**Related backlog tasks:**
- Create Flask app factory, configuration, and run entry point
- Implement live station API endpoint
- Implement historical station API endpoint
- Implement current, hourly, and daily weather API endpoints

**Prompt used:**
> In a Flask application, what is the best practice for structuring the App Factory pattern alongside multiple Blueprint routes for different API endpoints (e.g., /api/weather, /api/stations)?

**AI output summary:**
The AI provided a skeletal code structure demonstrating how to use `create_app()` to initialise the Flask app, configure the database connection, and register multiple Blueprints in a modular way to avoid circular imports.

**How the output was used:**
I adopted the Blueprint and App Factory conceptual pattern to keep our backend code modular and maintainable, effectively separating weather APIs from station APIs as required by my backlog tasks.

**Human review and modification:**
I did not copy the AI's exact code. I wrote the actual implementation myself to integrate securely with our specific `python-dotenv` configurations and custom database service query functions written by my teammates.

---

## Entry 4: Feature Engineering and Model Selection

**Related backlog tasks:**
- Prepare merged historical dataset for modelling
- Engineer time and weather features
- Train baseline and tree-based regression models

**Prompt used:**
> I have a merged dataset with timestamps, bike availability, and weather data. What are effective feature engineering techniques to capture cyclic time patterns and non-linear relationships for a regression model predicting bike numbers?

**AI output summary:**
The AI recommended extracting `hour`, `day_of_week`, and `month` from the timestamp to capture commuting patterns. It also suggested comparing a baseline Linear Regression model against tree-based models like Random Forest, noting that tree models handle non-linear weather interactions better.

**How the output was used:**
This confirmed my hypothesis that raw timestamps are unsuitable for standard regressors. I implemented the time-extraction logic using Pandas and trained both a baseline Linear Regression and a Random Forest Regressor for comparison.

**Human review and modification:**
The AI suggested complex trigonometric transformations for cyclic time (sine/cosine encoding). I decided this was over-engineering for our current scope and chose to keep the features as simple integers (e.g., hour 0-23), which proved sufficient for the Random Forest model to achieve a high R-squared score.

---

## Entry 5: EC2 Deployment Troubleshooting and Model Optimisation

**Related backlog tasks:**
- Evaluate models and save best model file
- Verify local app integration with database-backed APIs

**Prompt used:**
> We deployed our Flask app with a Random Forest model to an AWS EC2 instance. The backend crashes and freezes when the prediction route is hit （with some screenshots）. Please list the most likely causes and guide me through troubleshooting step-by-step.

**AI output summary:**
The AI listed several potential causes: incompatible Python versions, missing dependencies, or Out-Of-Memory (OOM) errors. It suggested checking the EC2 system logs (`dmesg -T | grep -i oom`) and using `htop` to monitor memory spikes during model loading.

**How the output was used:**
I used these Linux commands to diagnose our EC2 instance during integration verification. The `dmesg` command confirmed that the Linux kernel was killing our Flask process due to memory exhaustion (OOM), as we were using a `t2.micro` instance and the original model file was too large.

**Human review and modification:**
Once the root cause was identified, I independently implemented the solution: I re-evaluated the models, trained the Random Forest with strict pre-pruning (`max_depth=25`, `min_samples_split=20`), and saved the best model file using `joblib` compression. This reduced the file size to 21MB, resolving the EC2 memory crash.

---

## Entry 6: Prediction API Integration and Frontend Display

**Related backlog tasks:**

- Integrate model loading and prediction route into Flask app
- Add prediction controls and results display to frontend

**Prompt used:**
> How should I load a pre-trained model in a Flask backend to avoid latency? Should I load it globally or inside the route function every time a request is made?

**AI output summary:**
The AI strongly advised loading the model globally into memory when the Flask server starts (outside the route function) to eliminate file I/O overhead on every user request.

**How the output was used:**
I applied this architectural advice when integrating the model loading and prediction route. The model is loaded once at the top of the `api_db.py` Blueprint file, allowing the API to respond to frontend requests instantly.

**Human review and modification:**
The AI's example assumed static data. I had to write complex integration logic myself to dynamically parse the user's requested future time from the frontend prediction controls, fetch the nearest hourly weather forecast from our database, construct a Pandas DataFrame, and return the real-time prediction to be displayed on the UI.

## Reflection
GenAI was an invaluable sounding board for accelerating planning and diagnosing complex deployment issues like the EC2 OOM crash. However, its generic code suggestions lacked an understanding of our domain-specific database schema. Consequently, all machine learning and API integration code was manually rewritten, critically evaluated, and rigorously tested against our live system.