from utils.helpers import calc_distance

# =========================
# CONSTANTS
# Flight and fuel settings
# =========================
LAND_ARM_RADIUS = 50.0   # km
LAND_RADIUS = 0.3        # km
FUEL_PER_KM = 2.0        


# =========================
# PLANE CLASS
# Handles plane state and movement
# =========================
class Plane:
    def __init__(self, plane_id, airport):
        # Identity
        self.id = plane_id

        # Position
        self.current_airport = airport
        self.lat = airport.latitude
        self.lon = airport.longitude

        # State
        self.status = "parked"   # parked | flying
        self.destination = None

        # Fuel system
        self.max_fuel = 10000
        self.fuel = self.max_fuel

    # =========================
    # TAKEOFF
    # Change state to flying
    # =========================
    def take_off(self, destination_airport):
        if self.status != "parked":
            raise Exception("Plane not parked")

        self.status = "flying"
        self.destination = destination_airport
        self.current_airport = None

    # =========================
    # APPLY MOVEMENT (POSITION ONLY)
    # Update position and consume fuel
    # =========================
    def apply_movement(self, next_lat, next_lon):
        if self.status != "flying":
            return

        moved_km = calc_distance(
            self.lat,
            self.lon, 
            next_lat, 
            next_lon
        )
        
        fuel_cost = moved_km * FUEL_PER_KM

        if self.fuel < fuel_cost:
            raise Exception("Out of fuel")

        self.lat = next_lat
        self.lon = next_lon
        self.fuel -= fuel_cost

    # =========================
    # LANDING ZONE CHECK
    # Check if plane is close enough to land
    # =========================
    def can_land_at(self, airport, radius_km=LAND_ARM_RADIUS):
        distance = calc_distance(
            self.lat,
            self.lon,
            airport.latitude,
            airport.longitude
        )
        return distance <= radius_km

    # =========================
    # LAND
    # Complete landing at destination
    # =========================
    def land(self):
        if self.status != "flying":
            raise Exception("Plane not flying")

        landed = self.destination

        self.status = "parked"
        self.current_airport = landed
        self.lat = landed.latitude
        self.lon = landed.longitude
        self.destination = None

        return landed

    # =========================
    # REFUEL
    # Restore fuel to maximum
    # =========================
    def refuel(self):
        self.fuel = self.max_fuel

    # =========================
    # INFO
    # Public plane data
    # =========================
    def info(self):
        return {
            "id": self.id,
            "status": self.status,
            "lat": round(self.lat, 4),
            "lon": round(self.lon, 4),
            "fuel": round(self.fuel, 2),
            "current_airport": self.current_airport.code if self.current_airport else None,
            "destination": self.destination.code if self.destination else None
        }
