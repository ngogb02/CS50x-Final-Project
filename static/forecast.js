function isoTimeReformat(timeString) {
    const date = new Date(timeString);
    if (!isNaN(date)) {
        return date.toLocaleDateString('en-US', {hour: 'numeric', hour12: true});
    }
    return timeString
}

function sanitizeForId(value) {
    // Replace any character that is not a letter, digit, hyphen, or underscore with an underscore.
    return value.toString().trim().replace(/[^a-zA-Z0-9_-]/g, '_');
}

document.addEventListener('DOMContentLoaded', function() {
    // Reference to the formand forecast container
    const form = document.getElementById("userForm");
    // Use <main> as the container for forecast tabs
    const mainContainer = document.querySelector("main");
    
    // Add an event listener to the form to get the latitude and longitude when a user submits their lat/lon. 
    // By using "preventDefault()", it intercepts the submission and handle it with JS, instead of the default having the data go to the backend immediately. 
    // This technique is useful when you want to process or validate the form data on the client side before deciding whether to actually send the data to the server.
    form.addEventListener("submit", function(e) {
        e.preventDefault();

        // Get the user's inputs.
        const latitude = document.getElementById("latitude").value;
        const longitude = document.getElementById("longitude").value;
        // Could add verification of latitude and longitude in here...
    
    // Prepare the JSON payload.
    const requestData = {
        latitude: latitude,
        longitude: longitude,
    };

    // Optional: show a temporary loading message.
    const loadingMsg = document.createElement("p");
    loadingMsg.innerText = "Loading forecast...";
    mainContainer.appendChild(loadingMsg);

    fetch("/api/forecast", {
        method: "POST",
        header: {
            "Constant-Type": "application/json"
        },
        body: JSON.stringify(requestData)
    })
    .then(response => {
        // Remove the loading message.
        if (mainContainer.contains(loadingMsg)) {
            mainContainer.removeChild(loadingMsg);
        }
        if (!response.ok) {
            throw new Error("Server responded with ${response.statusText}");
        }
        return response.json();
    })
    .then(data => {
        // Create the <details> element to match the template.
        const detailsElem = document.createElement("details");
        detailsElem.classList.add("list-item");

        // Create the <summary> element for the header.
        const summaryElem = document.createElement("summary");
        summaryElem.classList.add("item-header")
        // Fill the innerText of the <summary> with the location's city name, state, and elevation, using the data from the backend server. 
        summaryElem.innerText = `${data.location.city || "Unknown City"}, ${data.location.state || "Unknown State"}, ${data.elevation.value || 0} Feet`;
        detailsElem.appendChild(summaryElem);

        // Create the <section> for the forecast content.
        const sectionElem = document.createElement("section");
        sectionElem.classList.add("item-content");

        // Create the container <div> for the forecast details.
        const divElem = document.createElement("div");
        divElem.classList.add("short_Forecast_12hr_7days");

        // Create the table for the forecast data.
        const tableElem = document.createElement("table");
        tableElem.classList.add("forecast_table");

        // 1st Row in the Table | region: Dates
        const trDates = document.createElement("tr");
        data.forecastdata_periods.forEach(period => {
            const th = document.createElement('th');
            th.textContent = period.name || "Unknown Name";
            trDates.appendChild(th);
        });
        tableElem.appendChild(trDates);

        // 2nd Row in the Table | region: Weather Icons and Mouse-Hover-Over-Icon for Detailed Forecast
        const trIcons = document.createElement("tr");
        data.forecastdata_periods.forEach(period => {
            const td = document.createElement("td");
            const tooltipDiv = document.createElement("div");
            tooltipDiv.classList.add("custom-tooltip");

            const imgElem = document.createElement("img");
            imgElem.id = "clickable_icon";
            imgElem.src = period.icon;
            imgElem.alt = "Weather Icon";

            const spanElem = document.createElement("span");
            spanElem.classList.add("tooltip_detailed_forecast");
            spanElem.textContent = period.detailedForecast || "";

            tooltipDiv.appendChild(imgElem);
            tooltipDiv.appendChild(spanElem);
            td.appendChild(tooltipDiv);
            trIcons.appendChild(td);
        });
        tableElem.appendChild(trIcons);

        // 3rd Row in the Table | region: Temperature
        const trTemperature = document.createElement("tr");
        data.forecastdata_periods.forEach(period => {
            const td = document.createElement("td");
            td.textContent = `${period.temperature || ""} ${period.temperatureUnit || ""}`;
            trTemperature.appendChild(td);
        });
        tableElem.appendChild(trTemperature);

        // 4th Row in the Table | region: Hours and Short Forecast
        const trHours = document.createElement("tr");
        data.forecastdata_periods.forEach(period => {
            const td = document.createElement("td");
            td.classList.add("centered_text");
            const spanTime = document.createElement("span");
            spanTime.classList.add("forecast_time");
            spanTime.textContent = `${isoTimeReformat(period.startTime)} - ${isoTimeReformat(period.endTime)}`;
            td.appendChild(spanTime);

            // Insert a <br> to separate the two spans, matching the HTML structure.
            td.appendChild(document.createElement("br"));

            const spanForecast = document.createElement("span");
            spanForecast.classList.add("forecast_text");
            spanForecast.textContent = period.shortForecast || "";
            td.appendChild(spanForecast);

            trHours.appendChild(td);
        });
        tableElem.appendChild(trHours);

        // Append the table to the forecast container 
        divElem.appendChild(tableElem);

        // Create the collapsible <div> for the Hourly Forecast 
        const hourlyForecastDiv = document.createElement("div");

        // Create the button
        const uniqueID = `collapse_plot_${sanitizeForId(data.latitude)}_${sanitizeForId(data.longitude)}`;
        const forecastButton = document.createElement("button");
        forecastButton.classList.add("btn", "btn-primary");
        forecastButton.setAttribute("type", "button");
        forecastButton.setAttribute("data-bs-toggle", "collapse");
        forecastButton.setAttribute("data-bs-target", `#${uniqueID}`);
        forecastButton.setAttribute("aria-expanded", "false");
        forecastButton.setAttribute("aria-controls", uniqueID);
        forecastButton.innerHTML = "Hourly Forecast";
        hourlyForecastDiv.appendChild(forecastButton);

        // Create the <div> that is target by the button
        const collapsePlotDiv = document.createElement("div");
        collapsePlotDiv.classList.add("collapse");
        collapsePlotDiv.id = uniqueID;

        // Create the <div> that contains the image
        const imageContainerDiv = document.createElement("div");
        imageContainerDiv.classList.add("image-container");

        const linkElem = document.createElement("a");
        linkElem.href = data.detailedForecastPlot_Image;
        linkElem.setAttribute("data-lightbox", "forecast");
        linkElem.setAttribute("data-title", "Detailed Forecast");

        const imgForecast = document.createElement("img");
        imgForecast.src = data.detailedForecastPlot_Image;
        imgForecast.atl = "Hourly Forecast";
        imgForecast.classList.add("img-fuild");

        linkElem.appendChild(imgForecast);
        imageContainerDiv.appendChild(linkElem);
        collapsePlotDiv.appendChild(imageContainerDiv);
        hourlyForecastDiv.appendChild(collapsePlotDiv);

        // Append Hourly Forecast to the <div class="short_Forecast_12hr_7days">
        divElem.appendChild(hourlyForecastDiv);

        sectionElem.appendChild(divElem);
        detailsElem.appendChild(sectionElem);

        // Append the new forecast tab to the <main> element. 
        mainContainer.appendChild(detailsElem);
    })
    .catch(error => {
        if (mainContainer.contains(loadingMsg)) {
            mainContainer.removeChild(loadingMsg);
        }
        console.error('Error fetching forecast:', error);
        alert("Error fetching forecast:" + error.message);
    });
 });
});


// https://copilot.microsoft.com/shares/1sc7eGe8QhWFpKbvvcagR

































})