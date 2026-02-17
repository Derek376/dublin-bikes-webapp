### 1. Map Page: Load the site and display the marker 
1. Given the user opens the map page, When station data loads successfully, Then <u>station markers are displayed</u> on the map.
2. Given station data is loading, When the request is in progress, Then the UI shows a <u>loading indicator</u>.
3. Given the stations request fails, When the failure happens, Then the UI shows a <u>clear error message</u>.

### 2. Click site marker: Pop-up window displays details
1. Given station markers are displayed, When the user clicks a station marker, Then a popup shows <u>station name</u>, <u>bikes available</u>, <u>free docks</u>, and <u>last updated time</u>.
2. Given the popup is open, When the user closes it, Then the popup disappears.
3. Given the data is older than a threshold (e.g., <u>10 minutes</u>), When the popup is shown, Then the UI indicates the data may be <u>outdated</u>.

### 3. Refresh site data (without refreshing the entire page)
1. Given the user is on the map page, When the user clicks <u>refresh</u>, Then the system requests the <u>latest station data</u>.
2. Given the refresh succeeds, When new data is received, Then the map <u>updates without a full page reload</u>.
3. Given the refresh fails, When the failure happens, Then the UI shows an <u>error message</u> and keeps the <u>previous data</u> visible.

### 4. Prediction
1. Given a station is selected, When the user requests prediction, Then the backend returns a <u>prediction result</u> for that station.
2. Given the prediction request succeeds, When the UI receives the result, Then the UI <u>displays the predicted value clearly</u>.
3. Given the prediction request fails, When the failure happens, Then the UI shows a <u>clear error message</u>.

### 5. Weather Display
1. Given the user opens the main page, When the weather request succeeds, Then the UI shows <u>temperature</u>, <u>rain/precipitation</u>, and <u>wind</u>
2. Given the weather request fails, When the failure happens, Then the UI shows <u>“Weather unavailable”</u> and the rest of the page still works.
3. Given weather data is older than a threshold (e.g., <u>30 minutes</u>), When it is displayed, Then the UI indicates it may be <u>outdated</u>.

### 6. JCDecaux Data Ingestion (Collection Job)
1. Given the ingestion job runs, When the JCDecaux API responds successfully, Then the system stores <u>station snapshots</u> in <u>MySQL</u> with <u>timestamps</u>.
2. Given the ingestion job encounters an API failure, When the failure happens, Then the system <u>logs the failure</u> and does <u>not insert incomplete records</u>.
3. Given stored snapshots exist, When a developer queries the database by <u>time range</u>, Then the correct records are returned.

### 7. OpenWeather Data Ingestion (Collection Job)
1. Given the ingestion job runs, When the OpenWeather API responds successfully, Then the system stores <u>weather snapshots</u> in <u>MySQL</u> with <u>timestamps</u>.
2. Given the weather API fails, When the failure happens, Then the system <u>logs the failure</u> and does <u>not insert incomplete records</u>.
3. Given stored weather data exists, When the backend requests recent weather, Then it can retrieve the <u>latest snapshot</u>.


### 8. Training Pipeline
1. Given the training pipeline runs, When training completes, Then a <u>model artifact</u> is saved (e.g., a joblib file).
2. Given evaluation runs, When it finishes, Then at least one metric (e.g., <u>MAE/RMSE</u>) is recorded for the report.
3. Given training is rerun with the same code and inputs, When it completes, Then the steps are <u>documented</u> so the process is <u>reproducible</u>.


### 9. EC2 Deployment
1. Given EC2 is running, When the demonstrator opens the <u>public URL</u>, Then the main page loads successfully.
2. Given the backend is deployed, When the demonstrator calls a core endpoint (e.g., <u>/api/stations</u>), Then it responds successfully from <u>EC2</u>.
3. Given deployment is complete, When a new team member reads the <u>README</u>, Then they can run the project locally and understand how to <u>deploy/restart</u> it.

### 10. User Registration and Login (Authentication)
1. Given the user registers with a valid email and password, When the account is created, Then the password is stored <u>securely (hashed)</u>, not plaintext.
2. Given the user logs in with correct credentials, When login succeeds, Then the user becomes <u>authenticated</u> for protected features.
3. Given the user enters invalid credentials, When login is attempted, Then the UI shows an <u>error message</u> and does not authenticate the user.

### 11. Favorites
1. Given the user is logged in, When the user adds a station to favorites, Then the station is saved and appears in the <u>favorites list</u>.
2. Given the user is logged in, When the user removes a station from favorites, Then it is removed from the <u>favorites list</u>.
3. Given the user is not logged in, When the user tries to use favorites, Then the system prompts login or returns <u>401 Unauthorized</u>.