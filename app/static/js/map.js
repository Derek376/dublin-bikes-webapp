let historyChart = null;
let weatherChart = null;
let activeMarker = null;
let activeInfoWindow = null;
let allMarkers = [];
let allStations = [];
let activeStationNumber = null;
let refreshIntervalId = null;
let isRefreshing = false;
let currentUser = null;
let currentStationIsFavorite = false;
let messageTimeout = null;
let currentFavorites = [];

/* =========================
   Message UI
========================= */

/**
 * Display a temporary status message in the UI.
 *
 * @param {string} type - Message type: success, error, or info.
 * @param {string} text - Message text to display.
 */
function showMessage(type, text) {
  const container = document.getElementById("message-container");
  const box = document.getElementById("message-box");
  const textEl = document.getElementById("message-text");

  if (!container || !box || !textEl) return;

  box.classList.remove("success", "error", "info");
  box.classList.add(type);

  textEl.textContent = text;
  container.classList.remove("hidden");

  if (messageTimeout) {
    clearTimeout(messageTimeout);
  }

  messageTimeout = setTimeout(() => {
    hideMessage();
  }, 3000);
}

/**
 * Hide the message box and clear any pending timeout.
 */
function hideMessage() {
  const container = document.getElementById("message-container");
  const box = document.getElementById("message-box");

  if (!container || !box) return;

  container.classList.add("hidden");
  box.classList.remove("success", "error", "info");

  if (messageTimeout) {
    clearTimeout(messageTimeout);
    messageTimeout = null;
  }
}

/* =========================
   Auth UI
========================= */

/**
 * Update the authentication status text in the UI.
 */
function updateAuthStatus() {
  const el = document.getElementById("auth-status-text");
  if (!el) return;

  if (currentUser) {
    el.textContent = `Logged in as ${currentUser.email}`;
  } else {
    el.textContent = "Not logged in";
  }
}

/* =========================
   Favorites UI
========================= */

/**
 * Update the state and label of the favorite toggle button.
 */
function updateFavoriteButton() {
  const btn = document.getElementById("favorite-toggle-btn");
  if (!btn) return;

  if (!activeStationNumber) {
    btn.disabled = true;
    btn.textContent = "Select a station first";
    return;
  }

  if (!currentUser) {
    btn.disabled = true;
    btn.textContent = "Login to add favorites";
    return;
  }

  btn.disabled = false;
  btn.textContent = currentStationIsFavorite
    ? "Remove from Favorites"
    : "Add to Favorites";
}

/**
 * Render the user's favorite stations list.
 *
 * @param {Array} favorites - List of favorite station objects.
 */
function renderFavoritesList(favorites) {
  const list = document.getElementById("favorites-list");
  if (!list) return;

  list.innerHTML = "";

  if (!favorites || favorites.length === 0) {
    list.innerHTML = "<li>No favorites yet.</li>";
    return;
  }

  favorites.forEach((item) => {
    const li = document.createElement("li");
    li.className = "favorite-item";
    li.style.cursor = "pointer";

    if (Number(item.station_number) === Number(activeStationNumber)) {
      li.classList.add("active");
    }

    li.innerHTML = `
      <strong>${item.name}</strong><br>
      <small>Station ${item.station_number} - ${item.address || "No address"}</small>
    `;

    li.addEventListener("click", () => {
      focusStationByNumber(item.station_number);
    });

    list.appendChild(li);
  });
}

/* =========================
   Refresh / status helpers
========================= */

/**
 * Update the refresh status badge.
 *
 * @param {string} status - Status value: idle, refreshing, success, or error.
 * @param {string|null} text - Optional custom text for the badge.
 */
function setRefreshStatus(status, text = null) {
  const el = document.getElementById("refresh-status");
  if (!el) return;

  el.className = `status-badge ${status}`;

  if (text) {
    el.textContent = text;
    return;
  }

  if (status === "idle") {
    el.textContent = "Idle";
  } else if (status === "refreshing") {
    el.textContent = "Refreshing...";
  } else if (status === "success") {
    el.textContent = "Up to date";
  } else if (status === "error") {
    el.textContent = "Refresh failed";
  }
}

/**
 * Update the "last updated" timestamp shown in the UI.
 */
function updateLastUpdatedTime() {
  const now = new Date();
  const formatted = now.toLocaleString([], {
    year: "numeric",
    month: "short",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
  });

  const el = document.getElementById("last-updated");
  if (el) {
    el.textContent = formatted;
  }
}

/**
 * Start periodic station data refresh.
 *
 * @param {number} intervalMs - Refresh interval in milliseconds.
 */
function startAutoRefresh(intervalMs = 60000) {
  if (refreshIntervalId) {
    clearInterval(refreshIntervalId);
  }

  refreshIntervalId = setInterval(() => {
    loadStations();
  }, intervalMs);
}

/* =========================
   Map / marker helpers
========================= */

/**
 * Remove all station markers from the map and reset active marker state.
 */
function clearAllMarkers() {
  allMarkers.forEach(({ marker }) => {
    marker.setMap(null);
  });

  allMarkers = [];
  activeMarker = null;

  if (activeInfoWindow) {
    activeInfoWindow.close();
    activeInfoWindow = null;
  }
}

/**
 * Get a marker color based on station bike availability.
 *
 * @param {number} availableBikes - Number of available bikes.
 * @param {number} totalStands - Total number of stands.
 * @returns {string} Marker color.
 */
function getMarkerColor(availableBikes, totalStands) {
  if (availableBikes == null || totalStands == null || totalStands === 0) {
    return "red";
  }

  const ratio = availableBikes / totalStands;

  if (ratio >= 0.6) return "green";
  if (ratio >= 0.3) return "orange";
  return "red";
}

/**
 * Build a Google Maps marker icon object.
 *
 * @param {string} color - Marker fill color.
 * @param {boolean} isActive - Whether the marker is currently selected.
 * @param {number} availableBikes - Number of available bikes.
 * @param {number} totalStands - Total number of stands.
 * @returns {Object} Google Maps symbol configuration.
 */
function createMarkerIcon(
  color,
  isActive = false,
  availableBikes = 0,
  totalStands = 0,
) {
  let baseScale = 8;

  if (totalStands > 0) {
    const ratio = availableBikes / totalStands;

    if (ratio >= 0.6) {
      baseScale = 10;
    } else if (ratio >= 0.3) {
      baseScale = 8;
    } else {
      baseScale = 6;
    }
  }

  return {
    path: google.maps.SymbolPath.CIRCLE,
    fillColor: color,
    fillOpacity: 0.9,
    strokeColor: "white",
    strokeWeight: isActive ? 2 : 1,
    scale: isActive ? baseScale + 4 : baseScale,
  };
}

/**
 * Check whether a station matches the selected filter.
 *
 * @param {Object} station - Station data object.
 * @param {string} filterValue - Current filter value.
 * @returns {boolean} True if the station should be shown.
 */
function matchesFilter(station, filterValue) {
  const availableBikes = station.available_bikes ?? 0;
  const totalStands =
    station.bike_stands ??
    availableBikes + (station.available_bike_stands ?? 0);

  const ratio = totalStands > 0 ? availableBikes / totalStands : 0;

  if (filterValue === "open") {
    return station.status === "OPEN";
  }

  if (filterValue === "high") {
    return ratio >= 0.6;
  }

  return true;
}

/**
 * Apply the current station filter to all map markers.
 */
function applyStationFilter() {
  const filterValue = document.getElementById("station-filter").value;

  allMarkers.forEach(({ marker, station }) => {
    if (matchesFilter(station, filterValue)) {
      marker.setMap(map);
    } else {
      marker.setMap(null);
    }
  });
}

/**
 * Restore the previously active station after markers are reloaded.
 *
 * @returns {boolean} True if the station was restored successfully.
 */
function restoreActiveStation() {
  if (activeStationNumber == null) {
    return false;
  }

  const target = allMarkers.find(
    ({ station }) => Number(station.number) === Number(activeStationNumber),
  );

  if (!target) {
    return false;
  }

  activateMarker(
    target.marker,
    target.marker.customColor,
    target.marker.customInfoWindow,
    target.station,
  );

  return true;
}

/**
 * Focus the map on a station by its station number.
 *
 * @param {number} stationNumber - Station number to focus.
 */
function focusStationByNumber(stationNumber) {
  const target = allMarkers.find(
    ({ station }) => Number(station.number) === Number(stationNumber),
  );

  if (!target) {
    showMessage("error", "Station not found on map");
    return;
  }

  const { marker, station } = target;
  const infoWindow = marker.customInfoWindow;
  const color = marker.customColor || "red";

  marker.setMap(map);
  activateMarker(marker, color, infoWindow, station);
  showMessage("info", `Showing ${station.name}`);
}

/**
 * Set a marker as active and load related station details and charts.
 *
 * @param {Object} marker - Google Maps marker instance.
 * @param {string} color - Marker color.
 * @param {Object} infoWindow - Marker info window.
 * @param {Object} station - Station data object.
 */
function activateMarker(marker, color, infoWindow, station) {
  if (activeInfoWindow) {
    activeInfoWindow.close();
  }

  if (activeMarker) {
    const previousColor = activeMarker.customColor || "red";
    const previousAvailableBikes = activeMarker.customAvailableBikes || 0;
    const previousTotalStands = activeMarker.customTotalStands || 0;

    activeMarker.setIcon(
      createMarkerIcon(
        previousColor,
        false,
        previousAvailableBikes,
        previousTotalStands,
      ),
    );
  }

  marker.setIcon(
    createMarkerIcon(
      color,
      true,
      marker.customAvailableBikes || 0,
      marker.customTotalStands || 0,
    ),
  );

  marker.customColor = color;

  activeMarker = marker;
  activeInfoWindow = infoWindow;
  activeStationNumber = station.number ?? null;

  renderFavoritesList(currentFavorites);

  infoWindow.open({
    anchor: marker,
    map: map,
  });

  map.panTo(marker.getPosition());

  if (map.getZoom() < 15) {
    map.setZoom(15);
  }

  updateStationDetails(station);

  if (station.number != null) {
    loadStationHistory(station.number);
  }

  loadWeatherForecast();
}

/* =========================
   Station detail / charts
========================= */

/**
 * Render selected station details in the side panel.
 *
 * @param {Object} station - Station data object.
 */
function updateStationDetails(station) {
  const detailsDiv = document.getElementById("station-details");

  const availableBikes = station.available_bikes ?? "N/A";
  const availableStands = station.available_bike_stands ?? "N/A";
  const totalStands = station.bike_stands ?? "N/A";

  detailsDiv.innerHTML = `
    <h2>${station.name || "Unknown Station"}</h2>
    <p><strong>Station Number:</strong> ${station.number ?? "N/A"}</p>
    <p><strong>Available Bikes:</strong> ${availableBikes}</p>
    <p><strong>Available Stands:</strong> ${availableStands}</p>
    <p><strong>Total Stands:</strong> ${totalStands}</p>
    <p><strong>Status:</strong> ${station.status ?? "N/A"}</p>
    <p><strong>Address:</strong> ${station.address ?? "N/A"}</p>
    <hr style="margin: 15px 0;">
    <h3 style="margin-bottom: 10px;">Predict Future Available Bikes</h3>
    <div style="display: flex; flex-direction: column; gap: 8px;">
      <input type="date" id="predict-date" style="padding: 5px;">
      <input type="time" id="predict-time" style="padding: 5px;">
      <button onclick="predictBikes(${station.number})" style="padding: 8px; cursor: pointer; background-color: #007bff; color: white; border: none; border-radius: 4px;">Run Prediction</button>
      <div id="predict-result" style="margin-top: 5px; font-weight: bold; color: #d9534f;"></div>
    </div>
  `;

  checkFavoriteStatus(station.number);
}

/**
 * Render the station history chart.
 *
 * @param {Array} historyData - Historical availability records.
 */
function renderHistoryChart(historyData) {
  const ctx = document.getElementById("historyChart").getContext("2d");

  const reversedData = [...historyData].reverse();

  const labels = reversedData.map((item) => {
    const dt = new Date(item.last_update);
    return dt.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
  });

  const availableBikesData = reversedData.map((item) => item.available_bikes);
  const availableStandsData = reversedData.map(
    (item) => item.available_bike_stands,
  );

  if (historyChart) {
    historyChart.destroy();
  }

  historyChart = new Chart(ctx, {
    type: "line",
    data: {
      labels: labels,
      datasets: [
        {
          label: "Available Bikes",
          data: availableBikesData,
          borderColor: "green",
          backgroundColor: "rgba(0,128,0,0.1)",
          tension: 0.3,
        },
        {
          label: "Available Stands",
          data: availableStandsData,
          borderColor: "orange",
          backgroundColor: "rgba(255,165,0,0.1)",
          tension: 0.3,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
    },
  });
}

/**
 * Load historical data for a station and update the chart.
 *
 * @param {number} stationNumber - Station number.
 */
async function loadStationHistory(stationNumber) {
  try {
    const response = await fetch(
      `/api/db/stations/${stationNumber}/history?limit=20`,
    );

    if (!response.ok) {
      throw new Error(`History fetch failed: ${response.status}`);
    }

    const historyData = await response.json();

    if (Array.isArray(historyData) && historyData.length > 0) {
      renderHistoryChart(historyData);
    } else if (historyChart) {
      historyChart.destroy();
      historyChart = null;
    }
  } catch (error) {
    console.error("Failed to load station history:", error);
  }
}

/**
 * Format a forecast datetime string for display.
 *
 * @param {string} dtString - Datetime string.
 * @returns {string} Formatted date and time string.
 */
function formatForecastTime(dtString) {
  const dt = new Date(dtString);
  return dt.toLocaleString([], {
    month: "short",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
}

/**
 * Render the weather forecast chart and summary card.
 *
 * @param {Array} forecastData - Forecast records.
 */
function renderWeatherForecast(forecastData) {
  const summaryDiv = document.getElementById("weather-summary");

  if (!Array.isArray(forecastData) || forecastData.length === 0) {
    summaryDiv.innerHTML = "<p>No weather forecast data available.</p>";

    if (weatherChart) {
      weatherChart.destroy();
      weatherChart = null;
    }
    return;
  }

  const topItems = forecastData.slice(0, 6);

  const labels = topItems.map((item) => formatForecastTime(item.future_dt));
  const tempData = topItems.map((item) => item.temp);
  const humidityData = topItems.map((item) => item.humidity);

  const ctx = document.getElementById("weatherChart").getContext("2d");

  if (weatherChart) {
    weatherChart.destroy();
  }

  weatherChart = new Chart(ctx, {
    type: "line",
    data: {
      labels: labels,
      datasets: [
        {
          label: "Temperature (°C)",
          data: tempData,
          borderColor: "blue",
          backgroundColor: "rgba(0, 0, 255, 0.1)",
          tension: 0.3,
          yAxisID: "y",
        },
        {
          label: "Humidity (%)",
          data: humidityData,
          borderColor: "purple",
          backgroundColor: "rgba(128, 0, 128, 0.1)",
          tension: 0.3,
          yAxisID: "y1",
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: {
          type: "linear",
          position: "left",
          title: {
            display: true,
            text: "Temperature (°C)",
          },
        },
        y1: {
          type: "linear",
          position: "right",
          title: {
            display: true,
            text: "Humidity (%)",
          },
          grid: {
            drawOnChartArea: false,
          },
        },
      },
    },
  });

  const first = topItems[0];

  summaryDiv.innerHTML = `
    <p><strong>Next Forecast Time:</strong> ${formatForecastTime(first.future_dt)}</p>
    <p><strong>Temperature:</strong> ${first.temp ?? "N/A"} °C</p>
    <p><strong>Humidity:</strong> ${first.humidity ?? "N/A"}%</p>
    <p><strong>Wind Speed:</strong> ${first.wind_speed ?? "N/A"} m/s</p>
    <p><strong>Weather ID:</strong> ${first.weather_id ?? "N/A"}</p>
  `;
}

/**
 * Load the latest hourly weather forecast from the backend.
 */
async function loadWeatherForecast() {
  try {
    const response = await fetch("/api/db/weather/hourly?limit=6");

    if (!response.ok) {
      throw new Error(`Weather fetch failed: ${response.status}`);
    }

    const forecastData = await response.json();
    renderWeatherForecast(forecastData);
  } catch (error) {
    console.error("Failed to load weather forecast:", error);

    document.getElementById("weather-summary").innerHTML =
      "<p>Failed to load weather forecast.</p>";

    if (weatherChart) {
      weatherChart.destroy();
      weatherChart = null;
    }
  }
}

/**
 * Update dashboard summary cards based on station data.
 *
 * @param {Array} stations - List of station objects.
 */
function updateSummaryCards(stations) {
  const totalStations = stations.length;

  const openStations = stations.filter(
    (station) => station.status === "OPEN",
  ).length;

  const totalBikes = stations.reduce(
    (sum, station) => sum + (station.available_bikes ?? 0),
    0,
  );
  const totalStands = stations.reduce(
    (sum, station) => sum + (station.available_bike_stands ?? 0),
    0,
  );

  document.getElementById("total-stations").textContent = totalStations;
  document.getElementById("open-stations").textContent = openStations;
  document.getElementById("total-bikes").textContent = totalBikes;
  document.getElementById("total-stands").textContent = totalStands;
}

/* =========================
   Auth API
========================= */

/**
 * Check the current authentication session and load user favorites.
 */
async function checkAuthStatus() {
  try {
    const response = await fetch("/auth/me");
    const data = await response.json();

    if (data.authenticated) {
      currentUser = data.user;
    } else {
      currentUser = null;
    }

    updateAuthStatus();
    await loadFavorites();
    updateFavoriteButton();
  } catch (error) {
    console.error("Failed to check auth status:", error);
  }
}

/**
 * Register a new user from the form inputs.
 */
async function registerUser() {
  const email = document.getElementById("register-email").value.trim();
  const password = document.getElementById("register-password").value;

  try {
    const response = await fetch("/auth/register", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password }),
    });

    const data = await response.json();

    if (!response.ok) {
      showMessage("error", data.error || "Registration failed");
      return;
    }

    currentUser = data.user;
    updateAuthStatus();
    await loadFavorites();
    updateFavoriteButton();
    showMessage("success", "Registration successful");
  } catch (error) {
    console.error("Registration failed:", error);
    showMessage("error", "Unable to register right now");
  }
}

window.predictBikes = async function (stationId) {
  const date = document.getElementById("predict-date")?.value;
  const time = document.getElementById("predict-time")?.value;
  const resultEl = document.getElementById("predict-result");

  if (!resultEl) {
    return;
  }

  if (!date || !time) {
    resultEl.innerHTML = "<span>Please select both date and time.</span>";
    return;
  }

  resultEl.textContent = "Loading prediction data...";

  try {
    const url = `/api/db/predict?station_id=${stationId}&date=${date}&time=${time}`;
    const response = await fetch(url);
    const data = await response.json();

    if (data.status === "success") {
      resultEl.textContent = `✅ Predicted available bikes: ${data.predicted_available_bikes} bikes`;
      return;
    }

    resultEl.textContent = "Prediction failed. Please try again.";
  } catch (error) {
    console.error("Prediction failed:", error);
    resultEl.textContent = "Prediction failed. Please try again.";
  }
};

/**
 * Log in a user from the form inputs.
 */
async function loginUser() {
  const email = document.getElementById("login-email").value.trim();
  const password = document.getElementById("login-password").value;

  try {
    const response = await fetch("/auth/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password }),
    });

    const data = await response.json();

    if (!response.ok) {
      showMessage("error", data.error || "Login failed");
      return;
    }

    currentUser = data.user;
    updateAuthStatus();
    await loadFavorites();
    updateFavoriteButton();
    showMessage("success", "Login successful");
  } catch (error) {
    console.error("Login failed:", error);
    showMessage("error", "Unable to login right now");
  }
}

/**
 * Log out the current user and clear related UI state.
 */
async function logoutUser() {
  try {
    const response = await fetch("/auth/logout", {
      method: "POST",
    });

    const data = await response.json();

    if (!response.ok) {
      showMessage("error", data.error || "Logout failed");
      return;
    }

    currentUser = null;
    currentStationIsFavorite = false;
    currentFavorites = [];
    updateAuthStatus();
    renderFavoritesList([]);
    updateFavoriteButton();
    showMessage("success", "Logout successful");
  } catch (error) {
    console.error("Logout failed:", error);
    showMessage("error", "Unable to logout right now");
  }
}

/* =========================
   Favorites API
========================= */

/**
 * Load the current user's favorite stations from the backend.
 */
async function loadFavorites() {
  if (!currentUser) {
    currentFavorites = [];
    renderFavoritesList([]);
    return;
  }

  try {
    const response = await fetch("/api/favorites");

    if (!response.ok) {
      if (response.status === 401) {
        currentUser = null;
        currentFavorites = [];
        updateAuthStatus();
        renderFavoritesList([]);
        return;
      }
      throw new Error("Failed to load favorites");
    }

    const favorites = await response.json();
    currentFavorites = favorites;
    renderFavoritesList(favorites);
  } catch (error) {
    console.error("Failed to load favorites:", error);
  }
}

/**
 * Check whether the selected station is in the user's favorites.
 *
 * @param {number} stationNumber - Station number to check.
 */
async function checkFavoriteStatus(stationNumber) {
  if (!stationNumber) {
    currentStationIsFavorite = false;
    updateFavoriteButton();
    return;
  }

  try {
    const response = await fetch(`/api/favorites/${stationNumber}/status`);
    const data = await response.json();

    currentStationIsFavorite = data.is_favorite || false;
    updateFavoriteButton();
  } catch (error) {
    console.error("Failed to check favorite status:", error);
  }
}

/**
 * Add or remove the active station from favorites.
 */
async function toggleFavorite() {
  if (!currentUser || !activeStationNumber) return;

  try {
    let response;

    if (currentStationIsFavorite) {
      response = await fetch(`/api/favorites/${activeStationNumber}`, {
        method: "DELETE",
      });
    } else {
      response = await fetch(`/api/favorites/${activeStationNumber}`, {
        method: "POST",
      });
    }

    const data = await response.json();

    if (!response.ok) {
      showMessage("error", data.error || "Favorite action failed");
      return;
    }

    const actionMessage = currentStationIsFavorite
      ? "Station removed from favorites"
      : "Station added to favorites";

    currentStationIsFavorite = !currentStationIsFavorite;
    updateFavoriteButton();
    await loadFavorites();
    showMessage("success", actionMessage);
  } catch (error) {
    console.error("Failed to toggle favorite:", error);
    showMessage("error", "Unable to update favorites right now");
  }
}

/* =========================
   Main data loading
========================= */

/**
 * Load live station data, rebuild markers, and refresh dashboard content.
 */
async function loadStations() {
  if (isRefreshing) {
    return;
  }

  isRefreshing = true;
  setRefreshStatus("refreshing");

  try {
    clearAllMarkers();

    const response = await fetch("/api/live/jcdecaux");

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const stations = await response.json();
    allStations = stations;
    allMarkers = [];

    updateSummaryCards(stations);

    let firstMarkerData = null;

    stations.forEach((station) => {
      const lat = station.position?.lat;
      const lng = station.position?.lng;

      if (lat == null || lng == null) {
        return;
      }

      const availableBikes = station.available_bikes ?? 0;
      const availableStands = station.available_bike_stands ?? 0;
      const totalStands =
        station.bike_stands ?? availableBikes + availableStands;
      const color = getMarkerColor(availableBikes, totalStands);

      const marker = new google.maps.Marker({
        position: { lat, lng },
        map: map,
        title: station.name || "Unknown Station",
        icon: createMarkerIcon(color, false, availableBikes, totalStands),
      });

      marker.customColor = color;
      marker.customAvailableBikes = availableBikes;
      marker.customTotalStands = totalStands;

      const infoWindow = new google.maps.InfoWindow({
        content: `
          <div style="min-width:220px">
            <h3 style="margin:0 0 8px 0;">${station.name || "Unknown Station"}</h3>
            <p><strong>Available Bikes:</strong> ${availableBikes}</p>
            <p><strong>Available Stands:</strong> ${availableStands}</p>
            <p><strong>Status:</strong> ${station.status ?? "N/A"}</p>
          </div>
        `,
      });

      marker.customInfoWindow = infoWindow;

      marker.addListener("click", () => {
        activateMarker(marker, color, infoWindow, station);
      });

      allMarkers.push({ marker, station });

      if (!firstMarkerData) {
        firstMarkerData = { marker, color, infoWindow, station };
      }
    });

    applyStationFilter();

    const restored = restoreActiveStation();

    if (!restored && firstMarkerData) {
      activateMarker(
        firstMarkerData.marker,
        firstMarkerData.color,
        firstMarkerData.infoWindow,
        firstMarkerData.station,
      );
    }

    updateLastUpdatedTime();
    setRefreshStatus("success");
  } catch (error) {
    console.error("Failed to load station data:", error);
    setRefreshStatus("error");
  } finally {
    isRefreshing = false;
  }
}

/* =========================
   App init
========================= */

/**
 * Initialize the Google Map, bind UI events, and load initial data.
 */
function initMap() {
  map = new google.maps.Map(document.getElementById("map"), {
    center: { lat: 53.3498, lng: -6.2603 },
    zoom: 13,
    mapTypeControl: false,
    streetViewControl: false,
    fullscreenControl: true,
  });

  const filterSelect = document.getElementById("station-filter");
  if (filterSelect) {
    filterSelect.addEventListener("change", applyStationFilter);
  }

  const registerBtn = document.getElementById("register-btn");
  const loginBtn = document.getElementById("login-btn");
  const logoutBtn = document.getElementById("logout-btn");
  const favoriteToggleBtn = document.getElementById("favorite-toggle-btn");
  const messageCloseBtn = document.getElementById("message-close-btn");

  if (registerBtn) {
    registerBtn.addEventListener("click", registerUser);
  }

  if (loginBtn) {
    loginBtn.addEventListener("click", loginUser);
  }

  if (logoutBtn) {
    logoutBtn.addEventListener("click", logoutUser);
  }

  if (favoriteToggleBtn) {
    favoriteToggleBtn.addEventListener("click", toggleFavorite);
  }

  if (messageCloseBtn) {
    messageCloseBtn.addEventListener("click", hideMessage);
  }

  setRefreshStatus("idle");
  checkAuthStatus();
  loadStations();
  startAutoRefresh(60000);
}

window.initMap = initMap;
