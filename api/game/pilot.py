# =========================
# PILOT CLASS
# Represents a game pilot
# =========================
class Pilot:
    def __init__(self, pilot_id: int, name: str, pilot_type="human"):
        # Identity data
        self.id = pilot_id
        self.name = name
        self.type = pilot_type

        # Pilot state
        self.active = False

    # =========================
    # LIFECYCLE
    # Pilot activation control
    # =========================
    def activate(self):
        self.active = True

    def deactivate(self):
        self.active = False

    # =========================
    # COMMANDS
    # Pilot-issued commands
    # =========================
    def command_takeoff(self, destination_airport):
        if not self.active:
            raise Exception("Pilot is not active")

        return {
            "action": "takeoff",
            "destination": destination_airport
        }

    # =========================
    # INFO
    # Pilot public information
    # =========================
    def info(self):
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type,
            "active": self.active
        }
