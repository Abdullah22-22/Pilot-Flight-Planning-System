import math
from utils.helpers import calc_distance
from game.game_manager import game_manager

# =========================
# CONTROL MODES
# =========================
MODE_AI = "AI"
MODE_MANUAL = "MANUAL"

# pilot_id -> control mode
_control_modes = {}

SPEED_KM_PER_TICK = 100.0
LAND_RADIUS = 0.3


# =========================
# MODE MANAGEMENT
# =========================
def get_mode(pilot_id: int) -> str:
    # Get current control mode for pilot
    return _control_modes.get(pilot_id, MODE_AI)


def set_mode(pilot_id: int, mode: str) -> None:
    # Set control mode (AI or MANUAL)
    if mode not in (MODE_AI, MODE_MANUAL):
        raise Exception("Invalid control mode")
    _control_modes[pilot_id] = mode


def set_ai(pilot_id: int) -> None:
    # Switch pilot to AI control
    set_mode(pilot_id, MODE_AI)


def set_manual(pilot_id: int) -> None:
    # Switch pilot to manual control
    set_mode(pilot_id, MODE_MANUAL)


# =========================
# AI MOVE (DECISION ONLY)
# =========================
def ai_next_move(plane):
    # AI decides next movement step
    if plane.status != "flying":
        return None

    if not plane.destination:
        return None

    distance = calc_distance(
        plane.lat,
        plane.lon,
        plane.destination.latitude,
        plane.destination.longitude
    )

    # Close enough → wait for landing
    if distance <= LAND_RADIUS:
        return None

    dlat = plane.destination.latitude - plane.lat
    dlon = plane.destination.longitude - plane.lon

    factor = SPEED_KM_PER_TICK / distance

    return {
        "action": "move",
        "next_lat": plane.lat + dlat * factor,
        "next_lon": plane.lon + dlon * factor
    }


# =========================
# MANUAL MOVE (DECISION ONLY)
# =========================
def manual_move(pilot_id, data):
    game = game_manager.get(pilot_id)
    if not game:
        raise Exception("Game not found")

    if get_mode(pilot_id) != MODE_MANUAL:
        raise Exception("Manual control not enabled")

    if game.plane.status != "flying":
        raise Exception("Plane is not flying")

    if not game.plane.destination:
        raise Exception("No destination set")

    if not data or "direction" not in data:
        raise Exception("direction required")

    direction = data["direction"]  # FORWARD | LEFT | RIGHT

    # ---- movement tuning (NO fuel here)
    STEP_KM = 5.0
    TURN_DEG = 5.0

    cur_lat = game.plane.lat
    cur_lon = game.plane.lon
    dest = game.plane.destination

    # Base heading toward destination
    dlat = dest.latitude - cur_lat
    dlon = dest.longitude - cur_lon
    base_heading = math.atan2(dlon, dlat)

    # Apply turn based on input
    if direction == "LEFT":
        heading = base_heading - math.radians(TURN_DEG)
    elif direction == "RIGHT":
        heading = base_heading + math.radians(TURN_DEG)
    elif direction == "FORWARD":
        heading = base_heading
    else:
        raise Exception("Invalid direction (FORWARD | LEFT | RIGHT)")

    # Move forward by fixed step
    KM_TO_DEG = 1 / 111.0
    delta_deg = STEP_KM * KM_TO_DEG

    next_lat = cur_lat + delta_deg * math.cos(heading)
    next_lon = cur_lon + delta_deg * math.sin(heading)

    game.handle_command({
        "action": "move",
        "next_lat": next_lat,
        "next_lon": next_lon
    })

    return game


# =========================
# GAME LOOP ENTRY
# =========================
def next_move_command(pilot_id: int, game):
    # Decide next move based on control mode
    if get_mode(pilot_id) == MODE_AI:
        if getattr(game, "waiting_for_landing", False):
            return None
        return ai_next_move(game.plane)

    # MANUAL → no automatic movement
    return None
