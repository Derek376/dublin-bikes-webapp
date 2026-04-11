let map;
let historyChart = null;
let weatherChart = null;
let activeMarker = null;
let activeInfoWindow = null;
let allMarkers = [];
let allStations = [];

function matchesFilter(station, filterValue) {
    const availableBikes = station.available_bikes ?? 0;
    const totalStands =
        station.bike_stands ?? (availableBikes + (station.available_bike_stands ?? 0));

    const ratio = totalStands > 0 ? availableBikes / totalStands : 0;

    if (filterValue === "open") {
        return station.status === "OPEN";
    }

    if (filterValue === "high") {
        return ratio >= 0.6;
    }

    return true;
}

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

function formatForecastTime(dtString) {
  const dt = new Date(dtString);
  return dt.toLocaleString([], {
    month: "short",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
}

function updateSummaryCards(stations) {
    const totalStations = stations.length;

    const openStations = stations.filter(
        station => station.status === "OPEN"
    ).length;

    const totalBikes = stations.reduce(
        (sum, station) => sum + (station.available_bikes ?? 0),
        0
    );

    const totalStands = stations.reduce(
        (sum, station) => sum + (station.available_bike_stands ?? 0),
        0
    );

    document.getElementById("total-stations").textContent = totalStations;
    document.getElementById("open-stations").textContent = openStations;
    document.getElementById("total-bikes").textContent = totalBikes;
    document.getElementById("total-stands").textContent = totalStands;
}

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

function getMarkerColor(availableBikes, totalStands) {
  if (availableBikes == null || totalStands == null || totalStands === 0) {
    return "red";
  }

  const ratio = availableBikes / totalStands;

  if (ratio >= 0.6) return "green";
  if (ratio >= 0.3) return "orange";
  return "red";
}

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
    `;
}

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
    } else {
      if (historyChart) {
        historyChart.destroy();
        historyChart = null;
      }
    }
  } catch (error) {
    console.error("Failed to load station history:", error);
  }
}

async function loadStations() {
  try {
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

      marker.addListener("click", () => {
        activateMarker(marker, color, infoWindow, station);
      });
      allMarkers.push({ marker, station });
      if (!firstMarkerData) {
        firstMarkerData = { marker, color, infoWindow, station };
      }
    });
    if (firstMarkerData) {
      activateMarker(
        firstMarkerData.marker,
        firstMarkerData.color,
        firstMarkerData.infoWindow,
        firstMarkerData.station,
      );
    }
    applyStationFilter();
  } catch (error) {
    console.error("Failed to load station data:", error);
    alert("Failed to load station data. Check console for details.");
  }
}

function initMap() {
    map = new google.maps.Map(document.getElementById("map"), {
        center: { lat: 53.3498, lng: -6.2603 },
        zoom: 13,
        mapTypeControl: false,
        streetViewControl: false,
        fullscreenControl: true
    });

    const filterSelect = document.getElementById("station-filter");
    if (filterSelect) {
        filterSelect.addEventListener("change", applyStationFilter);
    }

    loadStations();
}

window.initMap = initMap;
