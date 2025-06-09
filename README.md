# Weather Forecast: Weathernaut
#### Video Demo: <https://www.youtube.com/watch?v=AmbDNjH3Hl0>
#### Description:
<p>
This is a simple webpage that allows users to get percise weather forecast of their desired location[s] by inputting in the latitude and longitude of that exact spot. The latitude and longitude can be found via google map or other ways. Each forecast is shown up as a tab and can be expanded to view the detailed forecast. 
</p>

#### Inspiration:
<p>
This webpage was insipired by the NOAA (National Oceanic and Atmospheric Administration) weather forecast website. All of the weather forecast information displayed on this webpage was extracted from the NOAA Free API. <br> 
The main purpose of this site is not to present new or modified forecast information from the NOAA's page, but rather, it is a "one-stop shop" where the user can create a page that holds all of their desired forecast locations, without navigating through various pages, like they would, on the NOAA's website or other similar weather apps. 
</p>

## Table of Contents
1. [Description](#description)
2. [Inspiration](#inpiration)
3. [Built With](#built-with)
4. [Getting Started](#getting-started)
    * [Prerequisites](#prerequisites)
    * [Installation](#installation)
5. [Usage](#usage)
6. [System Description](#system-description)
7. [Roadmap](#roadmap)
8. [Contact](#contact)

## Built With
* [![Python][Python-Icon]][Python-url]

* [![HTML][HTML-Icon]][HTML-url]

* [![Javascript][JS-Icon]][JS-url]

* [![CSS][CSS-Icon]][CSS-url]

* [![Bootstrap][Bootstrap-Icon]][Bootstrap-url]

* [![Flask][Flask-Icon]][Flask-url]

* [![Sqlite3][Sqlite-Icon]][Sqlite3-url]

* [![DB-Browser][DB-Browser-Icon]][DB-Browser-url](DB Browsers for SQLite)

## Getting Started
<p>It is highly recommended to create a virtual environment for your local PC to run this project on. You will need to install python modules/packages/libraries.</p>

Run this cmd in the terminal to create a virtual environment "venv":
<br>
```
python -m venv {venv file name}
```
Make sure to activate or deactivate your venv as needed. When installing modules/packages/libraries, make sure the venv is activated, denoted by a green icon on the left of the current folder's directory. 

### Prerequisites:
<p>
The requirements.txt contains all of the python modules/packages/libraries that will be required for this project. 
To quickly install all of these, simply run this cmd in the terminal. Once again, remember to activate the venv before pip install.
</P>

```
pip install -r requirements.txt
```

### Installation:

It is highly recommended to use a database browser tool GUI to work with SQLite/DB. The one recommended for this project is [DB Browsers for SQLite][DB-Browser-Url].

## Usage
Find the latitude and longitude of your desired location, input it in the web's latitude and longitude text box and click on the "(+) Location" button. A minimized weather tabs of the location will appear, you can expand it by clicking on it to see the forecasts. 

## System Description

### Root:
### Python Files:
* app.py:
    * The Flask portion of this project lives inside the python file "app.py". 
    * This file handles all of the "POST" and "GET" request from the user.
    * This file also houses many functions used to call the external NOAA free API for forecast information.
    * The information from the NOAA API will then be inserted into a sqlite3 database.
    * This file directly calles the "graphUrl.py" file, which is used to contruct the hourly forecast image, then it returns the information back to "app.py" as an encoded message, also stored in the database.
    * The app will then query the database to render the page. 

* graphUrl.py:
    * This file only gets called by "app.py" during the process of calling the external NOAA API. 
    * This file will do 3 requests from the NOAA url to get the desired hourly forecast images (1 long image broken down into 3 parts).
    * It will then stitch or combine these 3 images side-by-side to create 1 large (horizontally) image and returns that back a ByteIO, or an in-memory with the format being a "PNG".  

### SQLite3 Database:
* database.db (forecasts):
    * Inside this db is a sqlite3 database named "forecasts" that houses all of the forecast information for each specific desired location by the user.
    * The database columns are as: id | lattitude | longitude | location | elevation | forecast_periods | detailedForecastPlot_Image | last_updated 
    * the id is a unique identifier that increment, and the database is a based on the composite key of latitude and longitude, so that the user can not create mutiple rows of the same location with slightly adjusted numbers in the latitude and/or longitude. 

    ### HTML:
    * Folder - templates:
        * index.html:
            * Inside the templates folder is the "index.html" file.
            * This file is responsible for the webpage's layout.
            * This file interacts with the backend server from Flask/app.py to transmit "GET" or "POST" requests. 
            * This file also calls all of the associated Javascript files (in the static folder).

    ### CSS and JS
    * Folder - static: 
        * style.css:
            * This file is mainly responsible for all of the styling in the html webpage.
        * forecast.js:
            * This file is responsible for intercepting the user's (+)Location submit button to call the backend api "/api/forecast" to fetch the external API for the forecast of the user's desired location and then store the information in the database, as mentioned above. 
            * After API call is complete, the JS file will use the newly added information in the database to build a new forecast tab, following the structure of the html, and insert it in the page (this eliminates the need for the whole page to refresh whenever need forecast is added).
        * delete_forecast.js:
            * This file is responsible for deleting the forecast tab when the user clicks the delete button on the webpage.
            * The JS will detect that the delete button has been clicked and then delete that forecast tab from the webpage without any reload.
            * It will then call the backend API "/api/delete_forecast" to delete that forecast info from the database. 
        * bootstrap_button_closed.js:
            * This file is reponsible for ensuring that when the user closes the main tab, if the Hourly Forecast tab was opened, it would also be closed, so that next time when the user opens the main tab, they would not see the Hourly Forecast tab already opened.   
            

## Roadmap
- [X] Add AJAX method to render weather tab without render entire page.
- [X] When Hourly Forecast tab is maximized, minimizing the main tab should also minimize the Hourly Forecast tab.
- [X] Add a button to delete weather forecast tab.
- [ ] Add a function to allow users to modify the name of the location and update the db to reflect the new name. Might be an issue on reload with the API refresh db. 
- [ ] Add dropdown or table with stored location's latitude/longitude.
- [ ] Add daily weather icons on the minimized weather tabs. 

## Contact

Bao G. Ngo - [Github/ngogb02](https://github.com/ngogb02) - ngogb02@gmail.com - https://www.linkedin.com/in/ngob2



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[Python-Icon]: https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54
[Python-url]: https://www.python.org/downloads/release/python-3132/

[HTML-Icon]: https://shields.io/badge/HTML-f06529?logo=html5&logoColor=white&labelColor=f06529
[HTML-url]: https://developer.mozilla.org/en-US/docs/Web/HTML

[JS-Icon]: https://shields.io/badge/JavaScript-F7DF1E?logo=JavaScript&logoColor=000&style=flat-square
[JS-url]: https://developer.mozilla.org/en-US/docs/Web/JavaScript

[CSS-Icon]: https://img.shields.io/badge/CSS-239120?&style=for-the-badge&logo=css3&logoColor=white
[CSS-url]: https://developer.mozilla.org/en-US/docs/Web/CSS

[Bootstrap-Icon]: https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white
[Bootstrap-url]: https://getbootstrap.com

[Flask-Icon]: https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=Flask&logoColor=white
[Flask-url]: https://flask.palletsprojects.com/en/stable/

[Sqlite-icon]: https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white
[Sqlite3-url]: https://www.sqlite.org/

[DB-Browser-Icon]: https://sqlitebrowser.org/images/sqlitebrowser.svg
[DB-Browser-url]: https://sqlitebrowser.org/