function magnify(imgID, zoom) {
    var img, glass, w, h, bw;
    img = document.getElementById(imgID);
  
    /* Create magnifier glass: */
    glass = document.createElement("DIV");
    glass.setAttribute("class", "img-magnifier-glass");
  
    /* Insert magnifier glass: */
    img.parentElement.insertBefore(glass, img);
  
    /* Set background properties for the magnifier glass: */
    glass.style.backgroundImage = "url('" + img.src + "')";
    glass.style.backgroundRepeat = "no-repeat";
    glass.style.backgroundSize = (img.width * zoom) + "px " + (img.height * zoom) + "px";
    bw = 3;
    w = glass.offsetWidth / 2;
    h = glass.offsetHeight / 2;
  
    /* Execute a function when someone moves the magnifier glass over the image: */
    glass.addEventListener("mousemove", moveMagnifier);
    img.addEventListener("mousemove", moveMagnifier);
  
    /*and also for touch screens:*/
    glass.addEventListener("touchmove", moveMagnifier);
    img.addEventListener("touchmove", moveMagnifier);

    function moveMagnifier(e) {
      var pos, x, y;
      
      /* Prevent any other actions that may occur when moving over the image */
      e.preventDefault();

      /* Get the cursor's x and y positions: */
      pos = getCursorPos(e);
      x = pos.x;
      y = pos.y;

      // Calculate scale factors based on natural vs displayed dimensions
      var scaleX = img.naturalWidth / img.width;
      var scaleY = img.naturalHeight / img.height;
        
      /* Prevent the magnifier glass from being positioned outside the image: */
      if (x > img.width - (w / zoom)) {x = img.width - (w / zoom);}
      if (x < w / zoom) {x = w / zoom;}
      if (y > img.height - (h / zoom)) {y = img.height - (h / zoom);}
      if (y < h / zoom) {y = h / zoom;}

      /* Set the position of the magnifier glass: */
      glass.style.left = (x - w) + "px";
      glass.style.top = (y - h) + "px";

      /* Display what the magnifier glass "sees": */
      glass.style.backgroundPosition = "-" + (((x * scaleX) * zoom) - w + bw) + "px -" + (((y * scaleY) * zoom) - h + bw) + "px";
    }
  
    function getCursorPos(e) {
      var a, x = 0, y = 0;
      e = e || window.event;
      /* Get the x and y positions of the image: */
      a = img.getBoundingClientRect();
      /* Calculate the cursor's x and y coordinates, relative to the image: */
      x = e.pageX - a.left;
      y = e.pageY - a.top;
      /* Consider any page scrolling: */
      x = x - window.pageXOffset;
      y = y - window.pageYOffset;
      return {x : x, y : y};
    }
  }

//#region Fetching via JS - Not in use.
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
//#endregion



