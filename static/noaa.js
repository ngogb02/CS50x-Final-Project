const latitude  = 47.402094608175815;
const longitude = -121.41549110412599;
const apiURL = `https://api.weather.gov/points/${latitude},${longitude}`;

async function fetchAPI_points() {
    const url = apiURL;
    try {
        console.log(apiURL);
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error(`fetchAPI_points Response status: ${response.status}`);
        }
        const points_json = await response.json();
        console.log('points_json:', points_json);
        return points_json;

    } catch (error) {
        console.error(`Error fetching data from ${url}:`, error?.message);
        throw error; 
    }
}

async function fetchAPI_ForecastData() {
    try {
        // call fetachAPI_points to get the json object that contains the forecast URL (API)
        const fetchPointsResponse = await fetchAPI_points();
        
        // Validate fetchAPI_points object contains the forecast data
        const forecastURL = fetchPointsResponse.properties.forecast; 
        if (!forecastURL) {
            throw new Error('forecastURL is missing or invalid.');
        }

        const response = await fetch(forecastURL);
        if (!response.ok) {
            throw new Error(`Request to forecast URL failed with status: ${response.status}`);
        }

        const forecast_json = await response.json();
        console.log('forecast_json:', forecast_json);
    } catch (error) {
        console.error('Error fetching data from forecast API:', error?.message);
        throw error;
    }
}
fetchAPI_ForecastData();




