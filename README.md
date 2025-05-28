# Weather Forecast: Weathernaut
#### Video Demo: <URL HERE>
#### Description:
<p>
This is a simple webpage that allows users to get percise weather forecast of their desired location[s] by inputting in the latitude and longitude of that exact spot. The latitude and longitude can be found via google map or other ways. Each forecast is shown up as a tab and can be expanded to view the detailed forecast. 
</p>

#### Inpiration:
<p>
This webpage was insipired by the NOAA (National Oceanic and Atmospheric Administration) weather forecast website. All of the weather forecast information displayed on this webpage was extracted from the NOAA Free API. <br> 
The main purpose of this site is not to present new or modified forecast information from the NOAA's page, but rather, it is a "one-stop shop" where the user can create a page that holds all of their desired forecast locations, without navigating through various pages.
</p>

## Table of Contents
1. [Description](#description)
2. [Inspiration](#inpiration)
3. [Built With](#built-with)
4. [Getting Started](#getting-started)
    * [Prerequisites](#prerequisites)
    * [Installation](#installation)
5. [Usage](#usage)
6. [Roadmap](#roadmap)
7. [Contact](#contact)

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
### Prerequisites
<p>
The requirements.txt contains all of the python modules/packages/libraries that will be required for this project. 
To quickly install all of these, simply run this cmd in the terminal. Once again, remember to activate the venv before pip install.
</P>

```
pip install -r requirements.txt
```

### Installation

It is highly recommended to use a database browser tool GUI to work with SQLite/DB. The one recommended for this project is [DB Browsers for SQLite][DB-Browser-Url].

## Usage
Find the latitude and longitude of your desired location, input it in the web's latitude and longitude text box and click on the "(+) Location" button. A minimized weather tabs of the location will appear, you can expand it by clicking on it to see the forecasts. 

## Roadmap
- [X] Add AJAX method to render weather tab without render entire page.
- [X] When Hourly Forecast tab is maximized, minimizing the main tab should also minimize the Hourly Forecast tab.
- [ ] Add a button to delete weather forecast tab.
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