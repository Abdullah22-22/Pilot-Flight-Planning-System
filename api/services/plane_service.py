from utils.helpers import calc_distance
from services.airport_service import find_refuel_airport
from game.airport import Airport


# =========================
# FLIGHT ROUTE PLANNER
# Plan full route with refuel stops if needed
# =========================
def plan_route(plane, final_dest, reserve_ratio=0.30, max_legs=3, stop_multiplier=0.5):
    # =========================
    # INITIAL VALIDATION
    # =========================
    # Plane must be parked at an airport
    start = plane.current_airport
    if start is None:
        return {
            "ok": False,
            "reason": "Plane not parked at an airport",
            "total_distance": 0,
            "legs": []
        }

    # =========================
    # FUEL & RANGE CALCULATION
    # =========================
    # Usable fuel range (keep reserve for safety)
    usable_range = plane.max_fuel * (1 - reserve_ratio)

    # Long-haul tuning values
    LONG_HAUL_RATIO = 0.6
    leg_limit = usable_range * stop_multiplier
    max_direct_distance = usable_range * LONG_HAUL_RATIO

    # =========================
    # ROUTE INITIALIZATION
    # =========================
    legs = [start]
    total_distance = 0.0

    current_lat = start.latitude
    current_lon = start.longitude
    dest = final_dest

    # =========================
    # ROUTE PLANNING LOOP
    # =========================
    # Try to reach destination within allowed legs
    for _ in range(max_legs):

        # Distance to final destination
        dist_to_dest = calc_distance(
            current_lat,
            current_lon,
            dest.latitude,
            dest.longitude
        )

        # =========================
        # DIRECT FLIGHT (SHORT HAUL)
        # =========================
        # Destination is reachable directly
        if dist_to_dest <= max_direct_distance:
            legs.append(dest)
            total_distance += dist_to_dest

            return {
                "ok": True,
                "reason": None,
                "total_distance": total_distance,
                "legs": legs
            }

        # =========================
        # REFUEL REQUIRED (LONG HAUL)
        # =========================
        # Find a refuel airport within safe range
        refuel = find_refuel_airport(
            current_lat,
            current_lon,
            dest.latitude,
            dest.longitude,
            leg_limit
        )

        if not refuel:
            return {
                "ok": False,
                "reason": "Long-haul flight requires refuel stop but none found",
                "total_distance": total_distance,
                "legs": legs
            }

        # =========================
        # BUILD REFUEL STOP AIRPORT
        # =========================
        # Convert database row to Airport object
        stop = Airport(
            refuel["ident"],
            refuel["name"],
            refuel["latitude_deg"],
            refuel["longitude_deg"],
            refuel["type"]
        )

        dist_to_stop = calc_distance(
            current_lat,
            current_lon,
            stop.latitude,
            stop.longitude
        )

        # =========================
        # SAFETY CHECK
        # =========================
        # Ensure stop is reachable safely
        if dist_to_stop > leg_limit:
            return {
                "ok": False,
                "reason": "Cannot reach refuel airport safely",
                "total_distance": total_distance,
                "legs": legs
            }

        # =========================
        # APPLY LEG
        # =========================
        # Add refuel stop as next leg
        legs.append(stop)
        total_distance += dist_to_stop

        # Update current position
        current_lat = stop.latitude
        current_lon = stop.longitude

    # =========================
    # MAX LEGS EXCEEDED
    # =========================
    # Route could not be planned within limits
    return {
        "ok": False,
        "reason": "Too many legs needed",
        "total_distance": total_distance,
        "legs": legs
    }
