from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
import requests

from .serializers import RouteRequestSerializer
from .services.router import get_route
from .services.fuel_loder import STATIONS   # ✅ fixed spelling
from .services.fuel_optimizer import plan_fuel_stops


def geocode(place):
    url = "https://nominatim.openstreetmap.org/search"
    params = {"q": place, "format": "json", "limit": 1, "countrycodes": "us"}
    headers = {"User-Agent": "fuel-planner"}

    r = requests.get(url, params=params, headers=headers, timeout=10)
    r.raise_for_status()

    data = r.json()
    if not data:
        raise ValueError(f"Location not found: {place}")

    return float(data[0]["lat"]), float(data[0]["lon"])


class RouteFuelAPIView(APIView):

    def post(self, request):
        serializer = RouteRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        start = serializer.validated_data["start"]
        finish = serializer.validated_data["finish"]

        try:
            # geocode
            s_lat, s_lon = geocode(start)
            e_lat, e_lon = geocode(finish)

            # routing (1 API call)
            geometry, distance = get_route(s_lat, s_lon, e_lat, e_lon)

            # convert OSRM lon,lat → lat,lon
            coords = [(c[1], c[0]) for c in geometry["coordinates"]]

            # sample to reduce computation
            sampled = coords[:: max(1, len(coords) // 300)]

            # fuel optimization
            stops, total_cost = plan_fuel_stops(sampled, distance, STATIONS)

            return Response({
                "start": start,
                "finish": finish,
                "distance_miles": round(distance, 2),
                "fuel_stops": stops,
                "total_cost": total_cost,
                "stations_considered": len(STATIONS),
                "route_geojson": geometry,
            })

        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response(
                {"error": "Something went wrong", "detail": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
