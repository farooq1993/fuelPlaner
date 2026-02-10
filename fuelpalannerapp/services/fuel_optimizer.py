from .geo import haversine

MAX_RANGE = 500
MPG = 10
SEARCH_RADIUS = 200


# find stations near route
def stations_near_route(route_points, stations):
    near = []
    for rp in route_points:
        lat, lon = rp
        for s in stations:
            d = haversine(lat, lon, s["lat"], s["lon"])
            if d <= SEARCH_RADIUS:
                near.append((rp, s))
    return near


def plan_fuel_stops(route_points, total_distance, stations):
    """
    Smart fuel planning:
    - find reachable stations
    - choose cheapest forward
    - buy minimum fuel if cheaper ahead
    """

    stops = []
    total_cost = 0

    current_index = 0
    fuel_left = MAX_RANGE

    while current_index < len(route_points) - 1:

        # can we reach destination?
        miles_left = (len(route_points) - current_index) * 5
        if miles_left <= fuel_left:
            break

        curr_lat, curr_lon = route_points[current_index]

        # find reachable stations
        reachable = []
        for i in range(current_index + 1, len(route_points)):
            dist = (i - current_index) * 5
            if dist > fuel_left:
                break

            rp = route_points[i]

            for s in stations:
                if haversine(rp[0], rp[1], s["lat"], s["lon"]) <= SEARCH_RADIUS:
                    reachable.append((i, dist, s))

        if not reachable:
            break

        # pick cheapest, if tie pick farthest
        reachable.sort(key=lambda x: (x[2]["price"], -x[1]))
        next_index, distance_to_station, station = reachable[0]

        # look ahead: is there cheaper further reachable after this?
        cheaper_ahead = False
        for r in reachable:
            if r[2]["price"] < station["price"]:
                cheaper_ahead = True
                break

        if cheaper_ahead:
            gallons = distance_to_station / MPG
        else:
            gallons = MAX_RANGE / MPG

        cost = gallons * station["price"]
        total_cost += cost

        stops.append({
            "name": station["name"],
            "lat": station["lat"],
            "lon": station["lon"],
            "price": station["price"],
            "gallons": round(gallons, 2),
            "cost": round(cost, 2),
        })

        fuel_left = MAX_RANGE
        current_index = next_index

    return stops, round(total_cost, 2)
