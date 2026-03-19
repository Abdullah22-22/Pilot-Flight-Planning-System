from flask import Blueprint, request, jsonify
from services import game_service, control_service

game_bp = Blueprint("game", __name__)

# =========================
# START GAME
# Create and initialize a new game
# =========================
@game_bp.route("/game/<int:pilot_id>/start", methods=["POST"])
def start_game(pilot_id):
    try:
        game = game_service.start_game(
            pilot_id,
            request.get_json(silent=True)
        )
        return jsonify({
            "message": "Game started",
            "status": game.status()
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# =========================
# PREVIEW ROUTE
# Show planned route without takeoff
# =========================
@game_bp.route("/game/<int:pilot_id>/preview", methods=["POST"])
def preview(pilot_id):
    try:
        game = game_service.preview_plane(
            pilot_id,
            request.get_json(silent=True)
        )
        return jsonify({
            "message": "Route preview ready",
            "status": game.status(),
            "route": [
                {"lat": ap.latitude, "lon": ap.longitude}
                for ap in game.flight_plan
            ]
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# =========================
# TAKEOFF
# Handle initial or next takeoff
# =========================
@game_bp.route("/game/<int:pilot_id>/takeoff", methods=["POST"])
def takeoff(pilot_id):
    try:
        game, message = game_service.takeoff(
            pilot_id,
            request.get_json(silent=True)
        )
        return jsonify({
            "message": message,
            "status": game.status()
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# =========================
# LAND
# Execute landing action
# =========================
@game_bp.route("/game/<int:pilot_id>/land", methods=["POST"])
def land(pilot_id):
    try:
        game, airport = game_service.land(pilot_id)
        return jsonify({
            "message": "Landed successfully",
            "airport": airport.code,
            "status": game.status()
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# =========================
# STATUS
# Get current game status
# =========================
@game_bp.route("/game/<int:pilot_id>/status", methods=["GET"])
def status(pilot_id):
    try:
        game = game_service.get_status(pilot_id)
        return jsonify({"status": game.status()})
    except Exception as e:
        return jsonify({"error": str(e)}), 404


# =========================
# ROUTE (MAP)
# Get route coordinates for map display
# =========================
@game_bp.route("/game/<int:pilot_id>/route", methods=["GET"])
def route(pilot_id):
    try:
        route = game_service.get_route(pilot_id)
        return jsonify({"route": route})
    except Exception as e:
        return jsonify({"error": str(e)}), 404


# =========================
# CONTROL MODE
# Switch between AI and MANUAL
# =========================
@game_bp.route("/game/<int:pilot_id>/mode/manual", methods=["POST"])
def enable_manual(pilot_id):
    try:
        control_service.set_manual(pilot_id)
        return jsonify({"message": "Manual mode enabled"})
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@game_bp.route("/game/<int:pilot_id>/mode/ai", methods=["POST"])
def enable_ai(pilot_id):
    try:
        control_service.set_ai(pilot_id)
        return jsonify({"message": "AI mode enabled"})
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# =========================
# MANUAL MOVE
# Apply manual movement command
# =========================
@game_bp.route("/game/<int:pilot_id>/manual/move", methods=["POST"])
def manual_move(pilot_id):
    try:
        game = control_service.manual_move(
            pilot_id,
            request.get_json(silent=True)
        )
        return jsonify({
            "message": "Manual move executed",
            "status": game.status()
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# =========================
# END GAME
# Remove game session
# =========================
@game_bp.route("/game/<int:pilot_id>", methods=["DELETE"])
def end_game(pilot_id):
    try:
        game_service.end_game(pilot_id)
        return jsonify({"message": "Game ended successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 404
