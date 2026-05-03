# GenAI Log — Jason Lee

## Project
COMP30830 Software Engineering — Dublin Bikes Occupancy and Weather Web Application with Machine Learning Prediction

## Student
Jason Lee

## Role in the Project

My main contributions to this project are: being responsible for requirements elicitation, i.e defining project objectives and target users, writing user stories, writing acceptance criteria, and preparing low-fidelity mockups. Frontend implementation - designing the UX and UI of the website, integrating Google Maps into the website, rendering station markers from backend data, applying occupancy-based marker styling, displaying information from backend - station information UI, weather information UI, favourites UI, chart creation and UI, live refresh functionality, UI based on user login status. I also contributed to documentation and report writing throughout the project.

## Overview of GenAI Use

Throughout the project, GenAI served as an idea generator and assistant debugger. During Sprint 1 it was consulted to help structure requirements artefacts, draft user stories and acceptance criteria. During Sprint 3 it was consulted for guidance on using the google Maps API, marker rendering approaches, panel update logic, and auth state handling in the frontend. AI generated content was reviewed to match the scope and objectives of our project.

---

## Entry 1: Defining Project Objectives and Target Users
**Related backlog tasks:**
- Define project objectives and target users

**Prompt used:**
> I am making a web application to display bike station and weather data. Who are the likely target users and what core objectives should we define for the project scope? 

**AI output summary:**
The AI suggested organising target users around usage patterns as opposed to demographics, e.g a daily commuter who wants fast and  reliable availability information, and a less frequent or tourist user who wants simpler at-a-glance information. It recommended framing objectives around real-time data accuracy and interface simplicity.

**How the output was used:**
The response helped structure the scope work around user needs rather than system features. The three personas developed — Henry (commuter student), Miguel (tourist), and Siobhán (operations analyst) — were informed by this framing. Each addressed real life issues such as arriving at an empty station.

**Human review and modification:**
The AI suggestions were generic and not specific to our project or the brief. All three personas were written by the team from scratch. The project objectives were also drafted independently and cross-checked against the project brief to confirm nothing was out of scope.

---

## Entry 2: Writing User Stories
**Related backlog tasks:**
- Write user stories for map, weather, auth, favourites, and prediction

**Prompt used:**
> We are writing user stories for a Dublin Bikes web application with the following features: a live station map, current weather display, user registration and login and saving favourite stations. Can you suggest a format and example stories for each of these features?

**AI output summary:**
The AI recommended the standard "As a [user], I want to [action], so that [benefit]" format aprovided example stories for each feature area covering the map, weather, authentication, favourites, and prediction.

**How the output was used:**
The format was adopted for all user stories in the backlog and report. The structure helped ensure each story was written from a user perspective with a clear benefit attached rather than describing a backend task.

**Human review and modification:**
The AI examples were generic and did not reflect the actual application. Each story was rewritten around what was being built. Stories referencing out-of-scope functionality such as email notifications or trip history were discarded. The final stories were mapped to the three distinct personas.

---

## Entry 3: Google Maps Integration and Station Marker Rendering

**Related backlog tasks:**
- Integrate Google Maps into homepage 
- Render station markers using backend data 

**Prompt used:**
> Our application should include a map integrated via the Google Maps JavaScript API, how do I ensure on load, that the map initialises correctly and is ready to receive live station marker data from a backend endpoint?

**AI output summary:**
The AI explained the standard approach for embedding the Maps API in an HTML template — loading the script with an async callback, initialising the map inside the callback to ensure the DOM and Maps library are both ready, and fetching station data separately after the map loads. It also prepped that the API keys should be not be hardcoded within the source code.

**How the output was used:**
The explanation confirmed the correct initialisation sequence. The final implementation used a window.initMap callback which initialised the map centred on Dublin with appropriate zoom and UI controls configured. After initialisation, live data is fetched the API endpoint and renders all markers. The API key was injected via Jinja2.

**Human review and modification:**
The AI used placeholder coordinates and a generic setup. The final initialization function set set the initial load to be centered on Dublin, it also bound all UI event listeners, keeping all event binding in one initialisation point as opposed to inline HTML onclick attributes as recommended.

---

## Entry 4: Occupancy-Based Marker Styling

**Related backlog tasks:**
- Style markers by occupancy level

**Prompt used:**
> How should I approach filtering the station markers based on bike availability levels so that users can immediately understand which stations have high, medium, or low availability?

**AI output summary:**
The AI suggested dividing availability into groups and assigning a distinct marker colour to each — green for high, amber for moderate, and red for low or empty.

**How the output was used:**
This approach was adopted. The percentage of bike availability was calculated inside the script and the appropriate icons were applied to the corresponding station. When clicked the markers would also be enlarged, giving a clear visual indication of the selected station. Similar logic would later be used for in marker filter.

**Human review and modification:**
The AI suggested using SVG path symbols for marker icons. The team instead used custom bike icon images. The active/inactive size distinction was a team design decision not suggested by the AI. The threshold values of were refined by the team for what felt the most useful from reading the map at a glance.

---

## Entry 5: Station Information/Weather Panel

**Related backlog tasks:**
- Add station detail panel on marker click 
- Display current weather summary and forecast panel

**Prompt used:**
> In a my web application, how should I update a sidebar panel with station details or weather information when a user clicks a marker? 

**AI output summary:**
The AI suggested handling station information through marker clicks and updating the innerHTML of already built panel with the data already attached to the marker. For weather it recommeneded fetaching the data on page load and using a innerHTML approach too.

**How the output was used:**
Approach was implemented, station detail panel renders relevent information such as available bikes and status on marker click. The weather panel fetches historical forecasts from the database and renders a text summary inside it's panel.


**Human review and modification:**
With minimal information UX design in mind. We changed the behaviour of the panels to show/hide based on whether they are clicked on or not, on page load station details are already checked. When unchecked the panel 'closes' only the panel title is shown. We also decided to create a visualization of the information and display them in the website. Charts were created and added to another panel at the bottom. To ensure that the website maintains its dimensions panels were changed to become scrollable based on how big the information was in the chart. 

## Entry 6: Favourites UI and Auth State Handling

**Related backlog tasks:**
- Display favourites and add user feedback states in UI

**Prompt used:**
> In a JavaScript frontend connected to a Flask backend, how should I handle user authentication state and conditionally show or hide features like favourites based on whether the user is logged in?

**AI output summary:**
The AI suggested checking authentication state on page load by calling a /me-style endpoint, storing the result in a module-level variable, and using that variable to conditionally render or enable/disable UI elements.

**How the output was used:**
Applying this logic, functions were wrote to check if a User was logged and saved to a module level variable. Features associated with favoriting were disabled if the user was not logged in. If logged in the favourite panel would update, fetching the data from the backend.

**Human review and modification:**
Additional UI elements were added to complement these features. Login and register UI was minimized into one modal. On login, a notification bar would notify if a user and display their login email. Favorited stations within the favorites panel were clickable and the map would zoom to the favorited station. The same notification bar would notify if when a user added or removed from the favorites panel. Removing favorites would also update the panel dynamically.

---

## Reflection
GenAI was used as a supporting tool across the requirements and frontend phases of the project. It was useful for brainstorming ideas for during the but the responses were either too broad and need to be refined to fit our project objectives. During frontend development, it proved very useful for frontend development and understanding errors in the javascript console. Particularly, in understanding the exact reponses/json of the API endpoints and understanding the the order in which functions should be called. The responses generated were somtimes too simple for use in the application and needed to be modified to fit the project requirements.