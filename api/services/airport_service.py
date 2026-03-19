from utils.helpers import calc_distance
from game.airport import Airport
from services.sql import fetch_refuel_airports, fetch_airport_by_code


# =========================
# FIND REFUEL AIRPORT
# Select best refuel stop on the way
# =========================
def find_refuel_airport(current_lat, current_lon, dest_lat, dest_lon, max_range):
    airports = fetch_refuel_airports()

    best = None
    best_dist = None

    for ap in airports:
        # Distance from current position to candidate airport
        d1 = calc_distance(
            current_lat, current_lon,
            ap["latitude_deg"], ap["longitude_deg"]
        )

        # Distance from candidate airport to final destination
        d2 = calc_distance(
            ap["latitude_deg"], ap["longitude_deg"],
            dest_lat, dest_lon
        )

        # Airport must be reachable with current fuel range
        if d1 <= max_range:
            # Choose airport that gets closer to destination
            if best is None or d2 < best_dist:
                best = ap
                best_dist = d2

    return best


# =========================
# GET AIRPORT BY CODE
# Fetch airport and map to domain object
# =========================
def get_airport_by_code(code: str):
    row = fetch_airport_by_code(code)

    if not row:
        return None

    # Map database row to Airport entity
    return Airport(
        code=row["ident"],
        name=row["name"],
        latitude=row["latitude_deg"],
        longitude=row["longitude_deg"],
        airport_type=row["type"]
    )
