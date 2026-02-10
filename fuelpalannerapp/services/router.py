import requests

def get_route(start_lat, start_lon, end_lat, end_lon):
    url = f"http://router.project-osrm.org/route/v1/driving/{start_lon},{start_lat};{end_lon},{end_lat}"
    params = {"overview": "full", "geometries": "geojson"}

    r = requests.get(url, params=params, timeout=10)
    r.raise_for_status()
    data = r.json()

    route = data["routes"][0]
    distance_miles = route["distance"] / 1609.34

    return route["geometry"], distance_miles
