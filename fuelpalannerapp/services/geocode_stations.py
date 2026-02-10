import pandas as pd
import requests
import time

INPUT = "D:\\fuelplanner\\fuelpalnnerproject\\fuelpalannerapp\\data\\fuel-prices-for-be-assessment.csv"
OUTPUT = "fuel_prices_geocoded.csv"

df = pd.read_csv(INPUT)
df.columns = [c.lower().strip() for c in df.columns]


def geocode(address):
    url = "https://nominatim.openstreetmap.org/search"
    params = {"q": address, "format": "json", "limit": 1, "countrycodes": "us"}
    headers = {"User-Agent": "fuel-planner"}

    try:
        r = requests.get(url, params=params, headers=headers, timeout=10)
        j = r.json()
        if j:
            return float(j[0]["lat"]), float(j[0]["lon"])
    except:
        pass
    return None, None


rows = []

# limit for fast demo
for i, row in df.head(300).iterrows():
    address = f"{row['address']}, {row['city']}, {row['state']}"
    lat, lon = geocode(address)

    if lat and lon:
        rows.append({
            "name": row["truckstop name"],
            "lat": lat,
            "lon": lon,
            "price": float(row["retail price"]),
        })

    time.sleep(1)

pd.DataFrame(rows).to_csv(OUTPUT, index=False)
print("Finished!")
