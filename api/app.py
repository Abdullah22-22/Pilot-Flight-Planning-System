from flask import Flask
from flask_cors import CORS

from routes.game_routes import game_bp
from routes.Location_Routes import location_bp
from services.game_loop import start_game_loop

# =========================
# FLASK APPLICATION SETUP
# =========================
app = Flask(__name__)

# =========================
# CORS CONFIGURATION
# =========================
CORS(app, resources={r"/*": {"origins": "*"}})

# =========================
# REGISTER BLUEPRINTS
# =========================
app.register_blueprint(game_bp)
app.register_blueprint(location_bp)

# =========================
# APPLICATION ENTRY POINT
# =========================
if __name__ == "__main__":
    # Start Game Loop ONCE
    start_game_loop()

    # Disable reloader to prevent double execution
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True,
        use_reloader=False
    )
