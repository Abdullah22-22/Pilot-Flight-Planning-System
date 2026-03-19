# =========================
# GAME MANAGER
# Responsible for managing all active games
# =========================
class GameManager:
    def __init__(self):
        # Store games using pilot_id as key
        self._games = {}

    def create(self, pilot_id, game):
        # Create a new game for a pilot
        if pilot_id in self._games:
            raise Exception("Game already exists")
        self._games[pilot_id] = game

    def get(self, pilot_id):
        # Get a game by pilot_id
        return self._games.get(pilot_id)

    def remove(self, pilot_id):
        # Remove and return a game by pilot_id
        return self._games.pop(pilot_id, None)

    def exists(self, pilot_id):
        # Check if a game exists for the pilot
        return pilot_id in self._games

    def all_items(self):
        # Return all games as (pilot_id, game) pairs
        return list(self._games.items())


# =========================
# SINGLETON INSTANCE
# Shared game manager for the whole app
# =========================
game_manager = GameManager()
