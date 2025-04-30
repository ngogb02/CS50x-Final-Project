import requests
import urllib.parse
import io
import re
from PIL import Image
from bs4 import BeautifulSoup

def getDetailedForecast(lat, lon):
    #-------------------------------------------------------Get the plot's URL---------------------------------------------------------------#
    url = f"https://forecast.weather.gov/MapClick.php?lat={lat}&lon={lon}&unit=0&lg=english&FcstType=graphical"
    baseUrl = "https://forecast.weather.gov/"

    # Get html content from detailed forecast page.
    response = requests.get(url)

    # Parse html
    soup = BeautifulSoup(response.text, "html.parser")

    # Find the the src that matches the regular expression. BeautifulSoup implicitly handles compiled regex - does not have to do .match()
    img_source = soup.find("img", src=re.compile("^meteograms"))["src"]

    # Combine the urls to produce the url needed to generate the detailedForecast graph image.
    img_weather = baseUrl + img_source

    #-------------------------------------------------------Image parsing URL----------------------------------------------------------------#

    # Time frame for adjusting "ahour" parameter in the img_weather url
    ahour = ["0", "48", "96"] 

    parsed_url = urllib.parse.urlparse(img_weather)

    query_params = urllib.parse.parse_qs(parsed_url.query)

    # Initialize the list
    img_url_3 = []

    for hour in ahour:

        # Parse the URL into components
        parsed_url = urllib.parse.urlparse(img_weather)

        # Extract the query parameters into a dictionary;
        # note: parse_qs returns values as lists for each key.
        query_params = urllib.parse.parse_qs(parsed_url.query)

        # Modify the 'ahour' parameter
        query_params["ahour"] = [hour]

        # Modify to show only snow, rain, temp, and wind/gust speed
        query_params["pcmd"] = ['10001000101000000000000000000000000000000000000000000000000']

        # Reassemble the query string; doseq=True ensures list values are handled correctly.
        new_query = urllib.parse.urlencode(query_params, doseq=True)

        # Rebuild the entire URL with the modified query parameters
        new_url = urllib.parse.urlunparse(parsed_url._replace(query=new_query))

        img_url_3.append(new_url)


    #-----------------------------------------------------------Image Concatenate-------------------------------------------------------------#

    img_response_list = [Image.open(BytesIO(requests.get(img).content)) for img in img_url_3]

    width_total = sum([img.width for img in img_response_list])
    combined = Image.new('RGB', (width_total, img_response_list[0].height))


    x_offset = 0
    for img in img_response_list:
        combined.paste(img, (x_offset,0))
        x_offset += img.width

    # Convert the stitched image to BytesIO.
    image_bytes = io.BytesIO()
    combined.save(image_bytes, format="PNG") # Writing data moves the pointer to the end.

    # Reset the pointer to the start.
    image_bytes.seek(0)

    # When returning, the pointer will start at the start and therefore able to point at the entire memory that contains the picture. 
    return BytesIO(combined)

if __name__ == "__main__":
    lat = 47.428
    lon = -121.418
    getDetailedForecast(lat, lon)
