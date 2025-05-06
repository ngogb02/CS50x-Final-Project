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

    #--------------------------------------------URL parsing for detailed forecast plots----------------------------------------------------#

    # Time frame for adjusting "ahour" parameter in the img_weather url
    ahour = ["0", "48", "96"] 
    # binary adjustments to only display snow, rain, temp, and wind/gust from NOAA detailed Forecast plot
    pcmd = "10001000101000000000000000000000000000000000000000000000000"

    # Returns a ParseResult object—a specialized tuple containing several fields: scheme, netloc, params, query
    parsed_url = urllib.parse.urlparse(img_weather)

    # The function urllib.parse.parse_qs takes that query string and splits it into key-value pairs (dictionary)
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
        query_params["pcmd"] = [pcmd]

        # Reassemble the query string; doseq=True ensures list values are handled correctly. Example: query_params = {"temp": ["20", "25"], "humidity": ["50"]} --> "temp=20&temp=25&humidity=50"
        new_query = urllib.parse.urlencode(query_params, doseq=True)

        # Rebuild the entire URL with the modified query parameters
        new_url = urllib.parse.urlunparse(parsed_url._replace(query=new_query))

        img_url_3.append(new_url)


    #-----------------------------------------------------------Image Concatenate (stitch)-------------------------------------------------------------#

    # For each URL (img), it uses requests.get(img) to send an HTTP GET request to retrieve the image data.
    # The .content attribute of the response provides the image data in bytes.
    # By wrapping these bytes with io.BytesIO, it creates an in-memory file-like object.
    # This step is crucial because it allows the PIL library to treat the raw bytes as if they were coming from a file.
    # Finally, Image.open() is called on this in-memory file object, which loads the image into a PIL Image object.
    # Each iteration of the list comprehension returns a PIL Image object, resulting in a list of images.
    img_response_list = [Image.open(io.BytesIO(requests.get(img).content)) for img in img_url_3]

    # Get the total width of all 3 images conbined 
    width_total = sum([img.width for img in img_response_list])

    # Create a new image called "combined" with the new width_total, and the height of the image (height didn't change)
    combined = Image.new('RGB', (width_total, img_response_list[0].height))

    # Iterate through the list of images, paste the first one at location (0, 0), second one shifted by the width of the image, and so on... (pasting onto the new image "combined" - blank canvas)
    x_offset = 0
    for img in img_response_list:
        combined.paste(img, (x_offset,0))
        x_offset += img.width

    # Test Code:
    # combined.show()

    # Convert the stitched image to BytesIO.
    image_bytes = io.BytesIO() # Create a new in-memory binary stream (RAM).
    combined.save(image_bytes, format="PNG") # Write the combined image to the allocated memory. Writing data moves the pointer to the end.

    # After writing, reset the pointer to the start of memory.
    image_bytes.seek(0)

    # When returning, the pointer will start at the start and therefore able to point at the entire memory that contains the picture. 
    return image_bytes

if __name__ == "__main__":
    lat = 47.428
    lon = -121.418
    getDetailedForecast(lat, lon)
