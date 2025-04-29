import requests
from bs4 import BeautifulSoup
import urllib.parse
from PIL import Image
from io import BytesIO

lat = 47.428
lon = -121.418
url = f"https://forecast.weather.gov/MapClick.php?lat={lat}&lon={lon}&unit=0&lg=english&FcstType=graphical"
baseUrl = "https://forecast.weather.gov/"

response = requests.get(url)

soup = BeautifulSoup(response.text, "html.parser")

img_source_list = [img['src'] for img in soup.find_all('img') if img['src'].startswith("meteograms")]
img_source = img_source_list[0]

img_weather = baseUrl + img_source

ahour = ["0", "48", "96"] 

parsed_url = urllib.parse.urlparse(img_weather)

query_params = urllib.parse.parse_qs(parsed_url.query)

#-------------------------------------------------------Image parsing URL--------------------------------------------------------------#

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


#-----------------------------------------------------------Image Stiching-------------------------------------------------------------#

img_response_list = [Image.open(BytesIO(requests.get(img).content)) for img in img_url_3]

width_total = sum([img.width for img in img_response_list])
combined = Image.new('RGB', (width_total, img_response_list[0].height))


x_offset = 0
for img in img_response_list:
    combined.paste(img, (x_offset,0))
    x_offset += img.width

combined.show()

# breakpoint()

