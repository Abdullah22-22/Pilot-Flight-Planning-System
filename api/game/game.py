from services.plane_service import plan_route


# =========================
# GAME CLASS
# Main game logic controller
# =========================
class Game:
    def __init__(self, pilot, plane):
        # Core objects
        self.pilot = pilot
        self.plane = plane

        # Game state flags
        self.active = False
        self.out_of_fuel = False

        # Flight planning data
        self.flight_plan = []
        self.current_leg = 0
        self.total_legs = 0
        self.final_destination = None

        # Flow control flags
        self.waiting_for_landing = False
        self.ready_for_takeoff = False
        self.initial_takeoff_done = False

        # Immutable trip data (for UI)
        self.trip_route = []
        self.trip_completed = False


    # =========================
    # GAME LIFECYCLE
    # Start the game session
    # =========================
    def start(self):
        self.active = True
        self.pilot.activate()

    # =========================
    # COMMAND HANDLER
    # Route incoming player commands
    # =========================
    def handle_command(self, command):
        if not self.active:
            raise Exception("Game not active")

        action = command.get("action")

        if action == "takeoff":
            self._handle_takeoff(command)

        elif action == "takeoff_next":
            self._handle_takeoff_next()

        elif action == "move":
            self._handle_move(command)

        else:
            raise Exception("Unknown command")

    # =========================
    # INITIAL TAKEOFF
    # Plan route and take off first leg
    # =========================
    def _handle_takeoff(self, command):
        if self.initial_takeoff_done:
            raise Exception("Flight already planned")

        if self.plane.status != "parked":
            raise Exception("Plane not parked")

        destination = command["destination"]

        plan = plan_route(self.plane, destination)
        if not plan["ok"]:
            raise Exception(f"Flight denied: {plan['reason']}")

        self.flight_plan = plan["legs"]
        self.total_legs = len(self.flight_plan) - 1
        self.current_leg = 1
        self.final_destination = destination

        # Save full route for frontend
        self.trip_route = [ap.code for ap in self.flight_plan]

        first_target = self.flight_plan[self.current_leg]
        self.plane.take_off(first_target)

        self.initial_takeoff_done = True

    # =========================
    # TAKEOFF AFTER REFUEL
    # Continue flight after landing
    # =========================
    def _handle_takeoff_next(self):
        if not self.ready_for_takeoff:
            raise Exception("Not ready for takeoff")

        if self.plane.status != "parked":
            raise Exception("Plane not parked")

        next_target = self.flight_plan[self.current_leg]
        self.ready_for_takeoff = False
        self.plane.take_off(next_target)

    # =========================
    # APPLY MOVEMENT
    # Called from control logic
    # =========================
    def _handle_move(self, command):
        if self.plane.status != "flying":
            return

        target = self.flight_plan[self.current_leg]

        # If plane reached landing zone → wait for landing
        if self.plane.can_land_at(target):
            self.waiting_for_landing = True
            return
        
        # Otherwise continue flying
        self.plane.apply_movement(
            command["next_lat"],
            command["next_lon"]
        )


    # =========================
    # CAN LAND
    # Check landing conditions
    # =========================
    def can_land(self):
        if not self.flight_plan or self.current_leg >= len(self.flight_plan):
            return False

        target = self.flight_plan[self.current_leg]

        return (
            self.waiting_for_landing
            and self.plane.status == "flying"
            and self.plane.can_land_at(target)
        )

    # =========================
    # LAND NOW
    # Execute landing process
    # =========================
    def land_now(self):
        if not self.can_land():
            raise Exception("Cannot land now")

        landed_airport = self.plane.land()

        # Refuel only at suitable airports
        if landed_airport.type in ("large_airport", "medium_airport"):
            self.plane.refuel()

        self.waiting_for_landing = False
        self.current_leg += 1

        # End of trip
        if self.current_leg >= len(self.flight_plan):
            self.trip_completed = True
            self._reset_flight()
            return landed_airport

        self.ready_for_takeoff = True
        return landed_airport

    # =========================
    # RESET FLIGHT
    # Clear flight data after completion
    # =========================
    def _reset_flight(self):
        self.flight_plan = []
        self.current_leg = 0
        self.total_legs = 0
        self.final_destination = None
        self.initial_takeoff_done = False
        self.ready_for_takeoff = False

    # =========================
    # STATUS
    # Frontend data contract
    # =========================
    def status(self):
        completed = self.trip_completed

        return {
            "game_active": self.active,
            "pilot": self.pilot.info(),
            "plane": self.plane.info(),
            "current_leg": self.current_leg,
            "total_legs": self.total_legs,

            "control_panel": {
                "can_land": self.can_land(),
                "can_takeoff": (
                    self.plane.status == "parked"
                    and (
                        not self.initial_takeoff_done   # initial takeoff
                        or self.ready_for_takeoff       # next leg takeoff
                    )
                ),
                "status_text": (
                    "Ready to land" if self.can_land()
                    else "Flying" if self.plane.status == "flying"
                    else "Ready for takeoff" if self.ready_for_takeoff
                    else "On ground"
                )
            },
            "trip_status": {
                "completed": completed,
                "pilot_name": self.pilot.name,
                "from": self.trip_route[0] if self.trip_route else None,
                "to": self.trip_route[-1] if self.trip_route else None,
                "stops": (
                    self.trip_route[1:-1]
                    if self.trip_route and len(self.trip_route) > 2
                    else []
                ),
                "fuel_remaining": round(self.plane.fuel, 2)
            }
        }
