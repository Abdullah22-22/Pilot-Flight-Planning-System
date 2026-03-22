from flask import Flask
from flask_cors import CORS

from routes.game_routes import game_bp
from routes.Location_Routes import location_bp
from services.game_loop import start_game_loop

app = Flask(__name__)

CORS(app, resources={
    r"/*": {
        "origins": [
            "http://localhost:3000",
            "http://localhost:5500",
            "http://127.0.0.1:5500",
            "http://127.0.0.1:3000",
            "https://pilot-flight-planning-system.vercel.app"
        ]
    }
})

@app.route("/")
def home():
    return {"status": "ok", "message": "Pilot Flight Planning System API is running"}

app.register_blueprint(game_bp)
app.register_blueprint(location_bp)

if __name__ == "__main__":
    start_game_loop()
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True,
        use_reloader=False
    )