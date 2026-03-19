import threading
import time
from game.game_manager import game_manager
from services.control_service import next_move_command

TICK_INTERVAL = 1.0  # seconds


# =========================
# MAIN GAME LOOP
# Runs continuously in background
# =========================
def _loop():
    while True:
        for pilot_id, game in game_manager.all_items():
            try:
                # Ask control service for next command
                cmd = next_move_command(pilot_id, game)
                if cmd:
                    # Execute command in game
                    game.handle_command(cmd)
            except Exception as e:
                # Prevent loop from stopping on errors
                print(f"[GAME LOOP] pilot={pilot_id} error={e}")

        # Wait until next tick
        time.sleep(TICK_INTERVAL)


# =========================
# START GAME LOOP
# Launch loop in daemon thread
# =========================
def start_game_loop():
    print("GAME LOOP STARTED")
    thread = threading.Thread(target=_loop, daemon=True)
    thread.start()
