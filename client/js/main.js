import { startGame, previewRoute } from "./api/gameApi.js";
import { startGameLoop } from "./core/gameLoop.js";
import { initMapAfterTakeoff } from "./map/mapController.js";
import { initControlModeButtons } from "./ui/controls.js";

// =========================
// CONFIG
// =========================
const PILOT_ID = 1;

const DEFAULT_GAME = {
  pilot_name: "Abdullah",
  plane_id: "JET-001",
  airport_code: null
};

let gameStarted = false;

// =========================
// READ ROUTE FROM SESSION
// =========================
const departureAirport = JSON.parse(
  sessionStorage.getItem("departureAirport")
);

const destinationAirport = JSON.parse(
  sessionStorage.getItem("destinationAirport")
);

// =========================
// AUTO START
// =========================
if (departureAirport && destinationAirport) {
  startGameAuto();
} else {
  window.location.href = "./location.html";
}

// =========================
// START GAME (NO AUTO TAKEOFF)
// =========================
async function startGameAuto() {
  if (gameStarted) return;
  gameStarted = true;

  // start game at departure airport
  DEFAULT_GAME.airport_code = departureAirport.ident;
  await startGame(PILOT_ID, DEFAULT_GAME);

  // preview route (draw line on map)
  await previewRoute(PILOT_ID, destinationAirport.ident);

  // store destination (used later for takeoff)
  sessionStorage.setItem(
    "pendingDestination",
    destinationAirport.ident
  );

  // init map (plane parked)
  await initMapAfterTakeoff(PILOT_ID);

  // init AI / Manual toggle buttons (ONCE)
  initControlModeButtons();

  // start polling game status
  startGameLoop(PILOT_ID);
}
