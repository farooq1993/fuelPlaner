import pandas as pd
from django.conf import settings
import os

DATA_PATH = os.path.join(
    settings.BASE_DIR,
    "fuelpalannerapp",
    "services",  # <-- your file is here
    "fuel_prices_geocoded.csv"
)

df = pd.read_csv(DATA_PATH)
df.columns = [c.lower().strip() for c in df.columns]

STATIONS = df.to_dict("records")

print("Stations loaded instantly:", len(STATIONS))
