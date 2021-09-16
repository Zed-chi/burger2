import requests
from geopy import distance

from geocache.models import Place


def get_coords(address):
    params = {"q": address, "polygon_geojson": 1, "format": "jsonv2"}

    result = requests.get(
        f"https://nominatim.geocoding.ai/search.php", params=params
    )
    result.raise_for_status()

    data = result.json()
    return float(data[0]["lat"]), float(data[0]["lon"])


def get_distance(order_place, restaurant_place):
    result = distance.distance(
        [order_place.lat, order_place.lon],
        [restaurant_place.lat, restaurant_place.lon],
    ).km
    return round(result, 2) if result else "... "


def get_place(address):
    coords = get_coords(address)
    print("coords ", coords)
    if not coords:
        coords = [0, 0]
    place = Place.objects.create(address=address, lat=coords[0], lon=coords[1])
    print("place ", place)
    return place
