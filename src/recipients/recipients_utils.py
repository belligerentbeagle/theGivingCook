from datetime import datetime
import requests
import urllib.parse
from streamlit_geolocation import streamlit_geolocation
from dotenv import load_dotenv
import os


def convert_address_to_latlong(address):
    load_dotenv()
    mapbox_token = os.getenv('MAPBOX_TOKEN')
    encoded_address = urllib.parse.quote(address)
    """Forward geocode an address to latitude and longitude."""
    url = f"https://api.mapbox.com/geocoding/v5/mapbox.places/{encoded_address}.json?access_token={mapbox_token}"

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data['features']:
            longitude, latitude = data['features'][0]['geometry']['coordinates']
            return latitude, longitude
        else:
            return None, None
    else:
        return None, None


def get_todays_date():
    return datetime.today().strftime('%Y-%m-%d')


def retrieve_current_location():
    location = streamlit_geolocation()
    res = [location["latitude"], location["longitude"]]

    return res
