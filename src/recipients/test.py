from geopy.geocoders import Nominatim
import geocoder
from geopy.exc import GeocoderTimedOut
from datetime import datetime
import requests
import urllib.parse


def forward_geocode(address):
    mapbox_token = "pk.eyJ1IjoiZ2Vva2xpbmdnZyIsImEiOiJjbTA3d2U1ejgwaTV0Mm1wdXplNHRlajd2In0.wb93FaNSef-op57WdTAnDw"
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


def reverse_geocode(lat, lon):
    mapbox_token = "pk.eyJ1IjoiZ2Vva2xpbmdnZyIsImEiOiJjbTA3d2U1ejgwaTV0Mm1wdXplNHRlajd2In0.wb93FaNSef-op57WdTAnDw"
    """Reverse geocode a latitude and longitude to an address."""
    url = f"https://api.mapbox.com/geocoding/v5/mapbox.places/{lon},{lat}.json"
    params = {
        "access_token": mapbox_token
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()  # Returns the full JSON response
    else:
        return None


def retrieveCurrentLocation():
    g = geocoder.ip('me')
    print(g.latlng)


def testAddress():
    def convertAddressToLatLong(address):
        geolocator = Nominatim(user_agent="theGivingCookApp")
        location = geolocator.geocode(address)
        if location:
            print(
                f"address {address}: lat: {location.latitude}, long: {location.longitude}")
            return (location.latitude, location.longitude)
        else:
            print(f"address {address}: not found")
            return (None, None)

    # List of test addresses
    test_addresses = [
        "520513",
        "529510",
        "238858",
    ]

    # Testing each address
    for address in test_addresses:
        convertAddressToLatLong(address)


def get_todays_date():
    return datetime.today().strftime('%Y-%m-%d')


if __name__ == "__main__":
    # testAddress()
    # retrieve_current_location()
    # retrieveAvailableInventory(get_todays_date())
    lat, long = forward_geocode(
        "4 Tampines Central 5, #01-47 Tampines Mall, Singapore 529510")
    print(f"successfully retrieved {lat} {long}")
