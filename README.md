# Fuel Route Planner API

This project provides a Django REST API that calculates the optimal fuel stops and total fuel cost for a trip between two locations in the USA.

The system uses real fuel price data, vehicle range constraints, and a routing engine to intelligently determine where refueling should occur.

---

## 🚀 Features

- Accepts start and finish locations (USA)
- Retrieves route geometry from OSRM (single API call)
- Determines optimal fuel stops based on price and reachability
- Assumes:
  - Maximum range: **500 miles**
  - Efficiency: **10 miles per gallon**
- Returns:
  - Route GeoJSON
  - Selected fuel stops
  - Total fuel cost
- Designed for **fast response times**
- Avoids excessive external API calls

---

## 🧠 Design Philosophy

External services are slow and unreliable.

Therefore:

- Fuel station geocoding is performed **offline**.
- The runtime API loads preprocessed data into memory.
- The live request makes only **one routing call**.

This ensures high performance and production readiness.

---

## 🏗 Architecture

Client (Postman)
↓
Django REST API
↓
Geocode start & finish (Nominatim)
↓
1 call → OSRM route
↓
In-memory fuel optimization
↓
Response JSON


---

## 📦 Tech Stack

- Python
- Django
- Django REST Framework
- OSRM (routing)
- Nominatim (geocoding)
- Pandas

---

## ⚙️ Setup

### 1. Install dependencies
pip install -r requirements.txt

### 2. Run makemigrations
python manage.py makemigrations
python manage.py migrate

### 3. Start server
python manage.py runserver


API Endpoint
POST /api/route/
curl --location 'http://127.0.0.1:8000/api/route/' \
--header 'Content-Type: application/json' \
--header 'Cookie: csrftoken=uwxt7XuwpypNLKdcyAMZCCIbNMOV18jK' \
--data '{"start": "Dallas, TX", "finish": "Kansas City, MO"}
'

Response

{
    "start": "Dallas, TX",
    "finish": "Kansas City, MO",
    "distance_miles": 496.58,
    "fuel_stops": [
        {
            "name": "7-Eleven #41830",
            "lat": 31.9667798,
            "lon": -95.2722825,
            "price": 2.91566666,
            "gallons": 50.0,
            "cost": 145.78
        },
        {
            "name": "SHORT STOP #13",
            "lat": 38.4040054,
            "lon": -96.181623,
            "price": 2.839,
            "gallons": 50.0,
            "cost": 141.95
        },
        {
            "name": "SHORT STOP #13",
            "lat": 38.4040054,
            "lon": -96.181623,
            "price": 2.839,
            "gallons": 50.0,
            "cost": 141.95
        }
    ],
    "total_cost": 429.68,
    "stations_considered": 50,
    "stations_considered": 50,
    "route_geojson": {
        "coordinates": [
            [
                -96.79675,
                32.775945
            ],
            [
                -96.797394,
                32.775797
            ],
            [
                -96.797462,
                32.77578
            ],
            [
                -96.797881,
                32.775684
            ],
            [
                -96.79794,
                32.77567
            ],
            [
                -96.798016,
                32.775795
            ],
            [
                -96.798063,
                32.775897
            ],
            [
                -96.798199,
                32.776302
            ],
            [
                -96.798228,
                32.776396
            ],
            [
                -96.798486,
                32.777183
            ],
            [
                -96.798489,
                32.77722
            ],
            [
                -96.798481,
                32.777298
            ],
            "type": "LineString"
    }
}