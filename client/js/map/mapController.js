import { getStatus, getRoute } from "../api/gameApi.js";
import { drawPlane, drawRoute, drawAirport } from "./mapRenderer.js";

// =========================
// MAP INITIALIZATION AFTER TAKEOFF
// =========================
export async function initMapAfterTakeoff(pilotId) {
  const routeRes = await getRoute(pilotId);
  const route = routeRes.route;

  // =========================
  // DRAW FLIGHT ROUTE
  // =========================
  drawRoute(route);

  if (!route || route.length < 2) return;

  // =========================
  // DRAW START AIRPORT
  // =========================
  drawAirport(
    route[0].lat,
    route[0].lon,
    "green",
    "start-airport"
  );

  // =========================
  // DRAW REFUEL / STOP AIRPORTS
  // =========================
  route.slice(1, -1).forEach((stop, index) => {
    drawAirport(
      stop.lat,
      stop.lon,
      "#000000ff", // stop airport marker color
      `stop-airport-${index}`
    );
  });

  // =========================
  // DRAW FINAL DESTINATION
  // =========================
  drawAirport(
    route[route.length - 1].lat,
    route[route.length - 1].lon,
    "red",
    "end-airport"
  );

  // =========================
  // DRAW PLANE INITIAL POSITION
  // =========================
  const status = await getStatus(pilotId);
  drawPlane(
    status.status.plane.lat,
    status.status.plane.lon
  );
}
