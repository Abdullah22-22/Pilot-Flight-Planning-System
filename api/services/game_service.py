from game.game import Game
from services.plane_service import plan_route
from game.game_manager import game_manager
from game.pilot import Pilot
from game.plane import Plane
from services.airport_service import get_airport_by_code


# =========================
# START GAME
# Create and start a new game
# =========================
def start_game(pilot_id, data):
    required = ["pilot_name", "plane_id", "airport_code"]
    if not data or not all(k in data for k in required):
        raise Exception("pilot_name, plane_id, airport_code required")

    if game_manager.exists(pilot_id):
        raise Exception("Game already exists for this pilot")

    airport = get_airport_by_code(data["airport_code"])
    if not airport:
        raise Exception("Airport not found")

    pilot = Pilot(pilot_id, data["pilot_name"])
    plane = Plane(data["plane_id"], airport)

    game = Game(pilot, plane)
    game.start()

    game_manager.create(pilot_id, game)
    return game


# =========================
# SHOW PLANE ON MAP
# Preview route without taking off
# =========================
def preview_plane(pilot_id, data):
    game = game_manager.get(pilot_id)

    if not game:
        raise Exception("Game not found")
    
    if not data or "destination_code" not in data:
        raise Exception("destination_code required")
    
    destination = get_airport_by_code(data["destination_code"])
    if not destination:
        raise Exception("Destination airport not found")
    
    if game.plane.status != "parked":
        raise Exception("Plane must be parked to preview route")
    
    plan = plan_route(game.plane, destination)
    if not plan["ok"]:
        raise Exception(f"Flight denied: {plan['reason']}")
    
    game.flight_plan = plan["legs"]
    game.total_legs = len(game.flight_plan) - 1
    game.current_leg = 0
    game.final_destination = destination
    game.trip_route = [ap.code for ap in game.flight_plan]

    return game


# =========================
# TAKEOFF (INITIAL + NEXT)
# Handle first and next takeoffs
# =========================
def takeoff(pilot_id, data=None):
    game = game_manager.get(pilot_id)
    if not game:
        raise Exception("Game not found")

    # Takeoff after refuel
    if game.ready_for_takeoff:
        game.handle_command({"action": "takeoff_next"})
        return game, "Takeoff to next leg"

    # Initial takeoff
    if not data or "destination_code" not in data:
        raise Exception("destination_code required")

    destination = get_airport_by_code(data["destination_code"])
    if not destination:
        raise Exception("Destination airport not found")

    game.handle_command({
        "action": "takeoff",
        "destination": destination
    })

    return game, "Initial takeoff initiated"


# =========================
# TICK
# Advance game logic by one tick
# =========================
def tick(pilot_id):
    game = game_manager.get(pilot_id)
    if not game:
        raise Exception("Game not found")

    game.handle_command({"action": "tick"})
    return game


# =========================
# LAND
# Execute landing
# =========================
def land(pilot_id):
    game = game_manager.get(pilot_id)
    if not game:
        raise Exception("Game not found")

    airport = game.land_now()
    return game, airport


# =========================
# STATUS
# Get current game status
# =========================
def get_status(pilot_id):
    game = game_manager.get(pilot_id)
    if not game:
        raise Exception("Game not found")

    return game


# =========================
# ROUTE (MAP)
# Get route coordinates for map
# =========================
def get_route(pilot_id):
    game = game_manager.get(pilot_id)
    if not game:
        raise Exception("Game not found")

    if not game.flight_plan:
        return []

    return [
        {"lat": ap.latitude, "lon": ap.longitude}
        for ap in game.flight_plan
    ]


# =========================
# END GAME
# Remove game and cleanup
# =========================
def end_game(pilot_id):
    game = game_manager.remove(pilot_id)
    if not game:
        raise Exception("Game not found")
