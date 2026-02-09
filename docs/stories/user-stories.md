# User Stories & Acceptance Criteria (Given / When / Then)

Tips:  We will add more stories later if needed.

---

## Persona: Henry (Commuter)

### H-01 Show bike stations on a map
**User Story**  
As a commuter, I want to see Dublin Bikes stations on an interactive map so that I can quickly choose a station.

**Acceptance Criteria**
1. Given the user opens the map page, When station data loads successfully, Then <u>station markers are displayed</u> on the map.
2. Given station data is loading, When the request is in progress, Then the UI shows a <u>loading indicator</u>.
3. Given the stations request fails, When the failure happens, Then the UI shows a <u>clear error message</u>.

---

### H-02 View station details
**User Story**  
As a commuter, I want to click a station and see <u>bikes available</u>, <u>free docks</u>, and <u>last updated time</u> so that I can trust the data.

**Acceptance Criteria**
1. Given station markers are displayed, When the user clicks a station marker, Then a popup shows <u>station name</u>, <u>bikes available</u>, <u>free docks</u>, and <u>last updated time</u>.
2. Given the popup is open, When the user closes it, Then the popup disappears.
3. Given the data is older than a threshold (e.g., <u>10 minutes</u>), When the popup is shown, Then the UI indicates the data may be <u>outdated</u>.

---

### H-03 Refresh station data
**User Story**  
As a commuter, I want to <u>refresh station data</u> so that I can see the latest availability.

**Acceptance Criteria**
1. Given the user is on the map page, When the user clicks <u>refresh</u>, Then the system requests the <u>latest station data</u>.
2. Given the refresh succeeds, When new data is received, Then the map <u>updates without a full page reload</u>.
3. Given the refresh fails, When the failure happens, Then the UI shows an <u>error message</u> and keeps the <u>previous data</u> visible.

---

### H-04 Request an occupancy prediction (ML / Required)
**User Story**  
As a commuter, I want to request a <u>short-term occupancy prediction</u> for a selected station so that I can plan around likely availability.

**Acceptance Criteria**
1. Given a station is selected, When the user requests prediction, Then the backend returns a <u>prediction result</u> for that station.
2. Given the prediction request succeeds, When the UI receives the result, Then the UI <u>displays the predicted value clearly</u>.
3. Given the prediction request fails, When the failure happens, Then the UI shows a <u>clear error message</u>.

---

## Persona: Miguel (Tourist)

### M-01 Show current weather
**User Story**  
As a tourist, I want to see <u>current weather</u> (temperature, rain, wind) so that I can decide whether cycling is a good option today.

**Acceptance Criteria**
1. Given the user opens the main page, When the weather request succeeds, Then the UI shows <u>temperature</u>, <u>rain/precipitation</u>, and <u>wind</u>.
2. Given the weather request fails, When the failure happens, Then the UI shows <u>“Weather unavailable”</u> and the rest of the page still works.
3. Given weather data is older than a threshold (e.g., <u>30 minutes</u>), When it is displayed, Then the UI indicates it may be <u>outdated</u>.

---

## Persona: Siobhán (Ops/Data Analyst)

### S-01 Store station snapshots in MySQL 
**User Story**  
As an operations analyst, I want station occupancy snapshots stored in <u>MySQL</u> so that the data is reliable and can be used for analysis.

**Acceptance Criteria**
1. Given the ingestion job runs, When the JCDecaux API responds successfully, Then the system stores <u>station snapshots</u> in <u>MySQL</u> with <u>timestamps</u>.
2. Given the ingestion job encounters an API failure, When the failure happens, Then the system <u>logs the failure</u> and does <u>not insert incomplete records</u>.
3. Given stored snapshots exist, When a developer queries the database by <u>time range</u>, Then the correct records are returned.

---

### S-02 Store weather snapshots in MySQL 
**User Story**  
As an operations analyst, I want weather snapshots stored in <u>MySQL</u> so that we can relate weather to station occupancy and support prediction.

**Acceptance Criteria**
1. Given the ingestion job runs, When the OpenWeather API responds successfully, Then the system stores <u>weather snapshots</u> in <u>MySQL</u> with <u>timestamps</u>.
2. Given the weather API fails, When the failure happens, Then the system <u>logs the failure</u> and does <u>not insert incomplete records</u>.
3. Given stored weather data exists, When the backend requests recent weather, Then it can retrieve the <u>latest snapshot</u>.

---

### S-03 Train and evaluate an ML model
**User Story**  
As an operations analyst, I want an ML model trained and evaluated on the provided historical dataset so that prediction performance is <u>measurable</u>.

**Acceptance Criteria**
1. Given the training pipeline runs, When training completes, Then a <u>model artifact</u> is saved (e.g., a joblib file).
2. Given evaluation runs, When it finishes, Then at least one metric (e.g., <u>MAE/RMSE</u>) is recorded for the report.
3. Given training is rerun with the same code and inputs, When it completes, Then the steps are <u>documented</u> so the process is <u>reproducible</u>.

---

## Cross-Persona / Delivery Requirements

### D-01 Deploy the application to EC2
**User Story**  
As a demonstrator, I want the application deployed on an <u>EC2 instance</u> with a <u>public URL</u> so that it can be evaluated remotely.

**Acceptance Criteria**
1. Given EC2 is running, When the demonstrator opens the <u>public URL</u>, Then the main page loads successfully.
2. Given the backend is deployed, When the demonstrator calls a core endpoint (e.g., <u>/api/stations</u>), Then it responds successfully from <u>EC2</u>.
3. Given deployment is complete, When a new team member reads the <u>README</u>, Then they can run the project locally and understand how to <u>deploy/restart</u> it.

---

### D-02 Register and login
**User Story**  
As a user, I want to <u>register and log in</u> so that I can access personalized features.

**Acceptance Criteria**
1. Given the user registers with a valid email and password, When the account is created, Then the password is stored <u>securely (hashed)</u>, not plaintext.
2. Given the user logs in with correct credentials, When login succeeds, Then the user becomes <u>authenticated</u> for protected features.
3. Given the user enters invalid credentials, When login is attempted, Then the UI shows an <u>error message</u> and does not authenticate the user.

---

### D-03 Save favorite stations
**User Story**  
As a logged-in user, I want to <u>save favorite stations</u> so that I can quickly check them later.

**Acceptance Criteria**
1. Given the user is logged in, When the user adds a station to favorites, Then the station is saved and appears in the <u>favorites list</u>.
2. Given the user is logged in, When the user removes a station from favorites, Then it is removed from the <u>favorites list</u>.
3. Given the user is not logged in, When the user tries to use favorites, Then the system prompts login or returns <u>401 Unauthorized</u>.